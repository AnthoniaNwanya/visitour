from fastapi import APIRouter

from api.controllers import tour_controller, visa_controller


travelrouter = APIRouter(
    prefix="/travel",
    tags=["Travels"],
)

travelrouter.post("/tours")(tour_controller.create_tour)
travelrouter.post("/visas")(visa_controller.create_visas)

travelrouter.get("/tours")(tour_controller.get_tours)
travelrouter.get("/tours/{travel_id}")(tour_controller.get_tour)
travelrouter.get("/visas")(visa_controller.get_visas)
travelrouter.get("/visas/{travel_id}")(visa_controller.get_visa)

travelrouter.put("/tours/{travel_id}")(tour_controller.update_tour)
travelrouter.put("/visas/{travel_id}")(visa_controller.update_visa)

travelrouter.delete("/tours/{travel_id}")(tour_controller.delete_tour)
travelrouter.delete("/visas/{travel_id}")(visa_controller.delete_visas)
