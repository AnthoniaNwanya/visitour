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
agencyrouter.get("/{agency_id}")(agency_controller.get_agency)

agencyrouter.put("/{agency_id}")(agency_controller.update_agency)

agencyrouter.delete(
    "/{agency_id}",
    response_model=DeleteAgencyResponse
    # status_code=204
)(agency_controller.delete_agency)
