from fastapi import APIRouter, Depends

from api.controllers import (
    agency_booking_controller,
    booking_controller,
    cart_controller,
    payment_controller,
)
from api.dependencies.authorization import (
    get_current_agency,
    get_current_traveler,
)
from schemas.dtos.booking_response import BookingResponse
from schemas.dtos.cart_response import CartResponse
from schemas.dtos.payment_response import PaymentResponse
from schemas.dtos.tour_booking_response import TourBookingResponse
from schemas.dtos.visa_booking_response import VisaBookingResponse


bookingrouter = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    dependencies=[Depends(get_current_traveler)],
)
cartrouter = APIRouter(
    prefix="/carts",
    tags=["Carts"],
    dependencies=[Depends(get_current_traveler)],
)
paymentrouter = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    dependencies=[Depends(get_current_traveler)],
)

bookingrouter.get("/", response_model=list[BookingResponse])(
    booking_controller.get_bookings
)
cartrouter.get("/", response_model=CartResponse | None)(
    cart_controller.get_cart
)
cartrouter.post("/items", response_model=CartResponse)(
    cart_controller.add_cart_item
)
cartrouter.put("/items/{item_id}", response_model=CartResponse | None)(
    cart_controller.update_cart_item
)
cartrouter.delete("/items/{item_id}", response_model=CartResponse | None)(
    cart_controller.delete_cart_item
)
paymentrouter.post("/", response_model=PaymentResponse)(
    payment_controller.create_payment
)
paymentrouter.get("/", response_model=list[PaymentResponse])(
    payment_controller.get_payments
)
paymentrouter.get("/{payment_id}", response_model=PaymentResponse)(
    payment_controller.get_payment
)
paymentrouter.put("/{payment_id}", response_model=PaymentResponse)(
    payment_controller.update_payment
)
paymentrouter.delete("/{payment_id}", status_code=204)(
    payment_controller.delete_payment
)

agencybookingrouter = APIRouter(
    prefix="/agency/bookings",
    tags=["Agency Bookings"],
    dependencies=[Depends(get_current_agency)],
)
agencybookingrouter.get("/tours", response_model=list[TourBookingResponse])(
    agency_booking_controller.get_tour_bookings
)
agencybookingrouter.get("/visas", response_model=list[VisaBookingResponse])(
    agency_booking_controller.get_visa_bookings
)
