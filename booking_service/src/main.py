from fastapi import FastAPI

from api.routers.routes import (
    agencybookingrouter,
    bookingrouter,
    cartrouter,
    paymentrouter,
)


app = FastAPI(
    title="Booking Service"
)

app.include_router(bookingrouter)
app.include_router(cartrouter)
app.include_router(paymentrouter)
app.include_router(agencybookingrouter)


@app.get("/")
def health_check():
    return {"message": "Booking Service is running"}
