from fastapi import APIRouter

from api.controllers import traveler


travelerrouter = APIRouter(
    prefix="/traveler",
    tags=["Travelers"],
)

travelerrouter.get("/")(traveler.get_travelers)
travelerrouter.get("/{traveler_id}")(traveler.get_traveler)
travelerrouter.post("/")(traveler.create_traveler)
travelerrouter.put("/{traveler_id}")(traveler.update_traveler)
travelerrouter.delete("/{traveler_id}")(traveler.delete_traveler)
