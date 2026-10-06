from fastapi import FastAPI

from api.routers.routes import travelrouter


app = FastAPI(
    title="Travel Service"
)

app.include_router(travelrouter)


@app.get("/")
def health_check():
    return {"message": "Travel Service is running"}
