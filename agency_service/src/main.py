from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.routes import agencyrouter
from media_storage import MEDIA_ROOT


app = FastAPI(
    title="Agency Service"
)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")
app.include_router(agencyrouter)


@app.get("/")
def health_check():
    return {"message": "Agency Service is running"}