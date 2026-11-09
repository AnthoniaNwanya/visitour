from fastapi import APIRouter
from api.controllers import agency_controller
from schemas.dtos.delete_agency_response import DeleteAgencyResponse


agencyrouter = APIRouter(
    prefix="/agency", 
    tags=["Agencies"]
    )

agencyrouter.post("/signup")(agency_controller.register_agency)
agencyrouter.post("/login")(agency_controller.login_agency)
agencyrouter.post("/validate-cac/{agency_id}")(agency_controller.validate_cac)


agencyrouter.get("/")(agency_controller.get_agencies)
agencyrouter.get("/profile")(agency_controller.get_agency_for_agency)
agencyrouter.get("/traveler/{traveler_id}")(
    agency_controller.get_traveler_for_agency
)

agencyrouter.put(
    "/edit",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "agency_name": {"type": "string"},
                            "description": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "phone_number": {"type": "string"},
                            "address": {"type": "string"},
                            "country": {"type": "string"},
                            "city": {"type": "string"},
                            "profilepicture": {
                                "type": "string",
                                "format": "binary",
                            },
                            "password": {"type": "string"},
                            "confirm_password": {"type": "string"},
                            "data": {
                                "type": "string",
                                "description": "Legacy JSON object. Prefer individual named fields.",
                            },
                        },
                    }
                },
                "application/json": {"schema": {"type": "object"}},
            },
        }
    },
)(agency_controller.update_agency)

agencyrouter.delete(
    "/delete",
    response_model=DeleteAgencyResponse
)(agency_controller.delete_agency)
