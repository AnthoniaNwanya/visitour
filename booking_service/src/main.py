from fastapi import FastAPI

from api.routers.routes import bookingrouter


app = FastAPI(
    title="Booking Service"
)

app.include_router(bookingrouter)


@app.get("/")
def health_check():
    return {"message": "Booking Service is running"}
