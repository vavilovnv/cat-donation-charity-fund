import multiprocessing

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import StandaloneApplication, settings
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    description=settings.app_desc
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()


if __name__ == '__main__':
    options = {
        "bind": f'{settings.project_host}:{settings.project_port}',
        "workers": multiprocessing.cpu_count(),
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    StandaloneApplication('main:app', options).run()
