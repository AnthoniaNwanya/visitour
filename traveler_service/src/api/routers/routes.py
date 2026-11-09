from fastapi import APIRouter

from api.controllers import traveler_controller


travelerrouter = APIRouter(
    prefix="/traveler",
    tags=["Travelers"],
)
agencyrouter = APIRouter(
    prefix="/agency",
    tags=["Agencies"],
)
travelerrouter.post("/signup")(traveler_controller.register_traveler)
travelerrouter.post("/login")(traveler_controller.login_traveler)

travelerrouter.get("/")(traveler_controller.get_travelers)  #protected but not for now
agencyrouter.get("/traveler/{traveler_id}")(
    traveler_controller.get_traveler_for_agency
)
travelerrouter.get("/profile")(traveler_controller.get_traveler_for_traveler)

travelerrouter.put(
    "/edit",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone_number": {"type": "string"},
                            "date_of_birth": {"type": "string", "format": "date"},
                            "address": {"type": "string"},
                            "city": {"type": "string"},
                            "country": {"type": "string"},
                            "nationality": {"type": "string"},
                            "status": {"type": "string"},
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
)(traveler_controller.update_traveler)

travelerrouter.delete("/delete")(traveler_controller.delete_traveler)
