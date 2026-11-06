from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.routers.routes import travelerrouter
from media_storage import MEDIA_ROOT


NOT_FOUND_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page not found | Traveler Service</title>
    <style>
      body { align-items: center; background: #f5f7fa; color: #172033; display: flex;
        font-family: system-ui, sans-serif; justify-content: center; margin: 0;
        min-height: 100vh; text-align: center; }
      main { max-width: 32rem; padding: 2rem; }
      h1 { font-size: 4rem; margin: 0; }
      p { color: #526078; line-height: 1.6; }
      a { color: #2457c5; }
    </style>
  </head>
  <body>
    <main>
      <h1>404</h1>
      <h2>Page not found</h2>
      <p>The route you requested doesn't exist in the Traveler Service.</p>
      <a href="/">Return to the service home</a>
    </main>
  </body>
</html>"""


app = FastAPI(
    title="Traveler Service"
)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")
app.include_router(travelerrouter)


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(
    request: Request,
    exc: StarletteHTTPException,
):
    if exc.status_code == 404 and request.scope.get("route") is None:
        return HTMLResponse(content=NOT_FOUND_PAGE, status_code=404)

    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.get("/")
def health_check():
    return {"message": "Traveler Service is running"}
