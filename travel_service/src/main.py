from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.routes import travelrouter
from media_storage import MEDIA_ROOT


app = FastAPI(
    title="Travel Service"
)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")
app.include_router(travelrouter)


@app.get("/")
def health_check():
    return {"message": "Travel Service is running"}
