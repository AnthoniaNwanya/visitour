from fastapi import APIRouter

from api.controllers import traveler_controller


travelerrouter = APIRouter(
    prefix="/traveler",
    tags=["Travelers"],
)

travelerrouter.post("/signup")(traveler_controller.register_traveler)
travelerrouter.post("/login")(traveler_controller.login_traveler)

travelerrouter.get("/")(traveler_controller.get_travelers)  #protected but not for now
travelerrouter.get("/agency/{traveler_id}")(
    traveler_controller.get_traveler_for_agency
)
travelerrouter.get("/profile")(traveler_controller.get_traveler_for_traveler)

travelerrouter.put("/edit")(traveler_controller.update_traveler)

travelerrouter.delete("/delete")(traveler_controller.delete_traveler)

