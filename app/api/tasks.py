from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.future import select
from app.schemas.task import TaskRequest, TaskStatusResponse, TaskResultResponse, TaskCreateResponse
from app.models.task import Task

tasks = APIRouter(prefix="/tasks")


async def fetch_task(task_id: int, request: Request):
    session = request.app.state.session
    query = await session.execute(select(Task).filter_by(id=task_id))
    task = query.scalars().first()
    await session.refresh(task)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@tasks.get('/{task_id}/status', response_model=TaskStatusResponse)
async def get_task_status(task: Task = Depends(fetch_task)):
    return {'status': task.status.name}


@tasks.get('/{task_id}/result', response_model=TaskResultResponse)
async def get_task_result(task: Task = Depends(fetch_task)):
    if not task.result:
        raise HTTPException(status_code=404, detail="Task result is not ready yet")
    else:
        return {'result': task.result}


@tasks.post('/', response_model=TaskCreateResponse, status_code=201)
async def create_task(payload: TaskRequest, request: Request):
    session = request.app.state.session
    task = Task(kind_id=payload.kind, data=payload.data)
    session.add(task)
    await session.flush()
    return {'id': task.id}
