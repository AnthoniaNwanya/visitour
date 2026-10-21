from fastapi import APIRouter
from api.controllers import tour_controller
from api.controllers import visa_application_controller
from schemas.dtos.delete_tour_response import DeleteTourResponse
from schemas.dtos.delete_visa_response import DeleteVisaResponse
from api.controllers import visa_type_controller

travelrouter = APIRouter(
    prefix="/travel",
    tags=["Travels"],
)

travelrouter.post("/tours/create")(tour_controller.create_tour)
travelrouter.post("/visa-applications/create")(visa_application_controller.create_visa_application)

travelrouter.get("/tours")(tour_controller.get_tours)
travelrouter.get("/tours/agency-tours")(tour_controller.get_my_agency_tours)
travelrouter.get("/visa-applications")(visa_application_controller.get_visa_applications)
travelrouter.get("/visa-applications/agency-visas")(visa_application_controller.get_my_agency_visa_applications)
travelrouter.get("/visa-types")(visa_type_controller.get_visa_types)

travelrouter.put("/tours/edit/{tour_id}")(tour_controller.update_tour)
travelrouter.put("/visa-applications/edit/{visa_id}")(visa_application_controller.update_visa_application)

travelrouter.delete("/tours/delete/{tour_id}", response_model=DeleteTourResponse)(tour_controller.delete_tour)
travelrouter.delete("/visa-applications/delete/{visa_id}", response_model=DeleteVisaResponse)(visa_application_controller.delete_visa_application)

