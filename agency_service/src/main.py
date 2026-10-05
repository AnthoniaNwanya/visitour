from fastapi import FastAPI

from api.routers.routes import agencyrouter


app = FastAPI(
    title="Agency Service"
)

app.include_router(agencyrouter)


@app.get("/")
def health_check():
    return {"message": "Agency Service is running"}