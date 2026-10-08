from fastapi import APIRouter

from api.controllers import tour_controller
from schemas.dtos.delete_tour_response import DeleteTourResponse

travelrouter = APIRouter(
    prefix="/travel",
    tags=["Travels"],
)

travelrouter.post("/tour")(tour_controller.create_tour)
# travelrouter.post("/visa")(visa_controller.create_visa)

travelrouter.get("/tour")(tour_controller.get_tours)
# travelrouter.get("/tour/{travel_id}")(tour_controller.get_tour)
# # travelrouter.get("/visa")(visa_controller.get_visas)
# # travelrouter.get("/visa/{travel_id}")(visa_controller.get_visa)

travelrouter.put("/tour/{tour_id}")(tour_controller.update_tour)
# # travelrouter.put("/visa/{travel_id}")(visa_controller.update_visa)

# travelrouter.delete("/tour/{travel_id}")(tour_controller.delete_tour)
travelrouter.delete(
    "/tour/{tour_id}",
    response_model=DeleteTourResponse
)(tour_controller.delete_tour)
# travelrouter.delete("/visa/{travel_id}")(visa_controller.delete_visa)
