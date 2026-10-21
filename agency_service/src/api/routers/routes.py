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

agencyrouter.put("/edit")(agency_controller.update_agency)

agencyrouter.delete(
    "/delete",
    response_model=DeleteAgencyResponse
)(agency_controller.delete_agency)
