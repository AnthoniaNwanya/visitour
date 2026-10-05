from fastapi import APIRouter
from api.controllers import agency
from schemas.dtos.delete_agency_response import DeleteAgencyResponse


agencyrouter = APIRouter(
    prefix="/agency", 
    tags=["Agencies"]
    )


agencyrouter.post("/signup")(agency.register_agency)
agencyrouter.post("/login")(agency.login_agency)
agencyrouter.post("/validate-cac/{agency_id}")(agency.validate_cac)


agencyrouter.get("/")(agency.get_agencies)
agencyrouter.get("/{agency_id}")(agency.get_agency)

agencyrouter.put("/{agency_id}")(agency.update_agency)

agencyrouter.delete(
    "/{agency_id}",
    response_model=DeleteAgencyResponse
    # status_code=204
)(agency.delete_agency)
