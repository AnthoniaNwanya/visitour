from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.routes import travelerrouter
from media_storage import MEDIA_ROOT


app = FastAPI(
    title="Traveler Service"
)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")
app.include_router(travelerrouter)


@app.get("/")
def health_check():
    return {"message": "Traveler Service is running"}
