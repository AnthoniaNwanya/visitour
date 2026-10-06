from fastapi import APIRouter

from api.controllers import booking


bookingrouter = APIRouter(
    prefix="/booking",
    tags=["Bookings"],
)

bookingrouter.get("/")(booking.get_bookings)
bookingrouter.get("/{booking_id}")(booking.get_booking)
bookingrouter.post("/")(booking.create_booking)
bookingrouter.put("/{booking_id}")(booking.update_booking)
bookingrouter.delete("/{booking_id}")(booking.delete_booking)
