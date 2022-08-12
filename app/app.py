from fastapi import FastAPI
from asyncio import create_task

from app.api.tasks import tasks
from app.db.core import async_session
from app.db.manage import init_db
from app.worker import Worker

app = FastAPI()


def create_app():
    app.include_router(tasks)
    return app


@app.on_event("startup")
async def on_startup():
    session = async_session()
    await init_db(session)
    app.state.session = session
    app.state.worker = Worker(session)
    create_task(app.state.worker.run())


@app.on_event("shutdown")
async def on_shutdown():
    app.state.worker.stop()
    await app.state.session.close()
