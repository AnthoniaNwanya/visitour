from fastapi import APIRouter

from api.controllers import traveler_controller


travelerrouter = APIRouter(
    prefix="/traveler",
    tags=["Travelers"],
)

travelerrouter.post("/signup")(traveler_controller.register_traveler)
travelerrouter.post("/login")(traveler_controller.login_traveler)

travelerrouter.get("/")(traveler_controller.get_travelers)


travelerrouter.put("/")(traveler_controller.update_traveler)

travelerrouter.delete("/")(traveler_controller.delete_traveler)

