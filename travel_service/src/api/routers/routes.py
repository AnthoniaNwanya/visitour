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

travelrouter.post("/tours")(tour_controller.create_tour)
travelrouter.post("/visa-applications")(visa_application_controller.create_visa_application)

travelrouter.get("/tours")(tour_controller.get_tours)
travelrouter.get("/visa-applications")(visa_application_controller.get_visa_applications)
travelrouter.get("/visa-types")(visa_type_controller.get_visa_types)

travelrouter.put("/tours/{tour_id}")(tour_controller.update_tour)
travelrouter.put("/visa-applications/{visa_id}")(visa_application_controller.update_visa_application)

travelrouter.delete("/tours/{tour_id}", response_model=DeleteTourResponse)(tour_controller.delete_tour)
travelrouter.delete("/visa-applications/{visa_id}", response_model=DeleteVisaResponse)(visa_application_controller.delete_visa_application)

