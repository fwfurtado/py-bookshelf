import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from src.controllers import author_controller
from src.entities import DB_URL


def init_app():
    custom_app = FastAPI()
    custom_app.add_middleware(
        PrometheusMiddleware, app_name="bookshelf", group_paths=True
    )
    custom_app.add_middleware(DBSessionMiddleware, db_url=DB_URL)
    custom_app.add_route("/metrics", handle_metrics)
    custom_app.include_router(author_controller.router)

    return custom_app


def start_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        debug=True,
        reload=True,
        log_level="debug",
    )


app = init_app()

if __name__ == "__main__":
    start_server()
