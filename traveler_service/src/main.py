from fastapi import FastAPI

from api.routers.routes import travelerrouter


app = FastAPI(
    title="Traveler Service"
)

app.include_router(travelerrouter)


@app.get("/")
def health_check():
    return {"message": "Traveler Service is running"}
