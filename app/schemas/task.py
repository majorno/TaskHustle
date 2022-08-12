from pydantic import BaseModel, Field
from app.models.kind import TaskKind


class TaskRequest(BaseModel):
    kind: int = Field(ge=int(TaskKind.REVERSE), le=int(TaskKind.REPEAT))
    data: str = Field(min_length=1)


class TaskCreateResponse(BaseModel):
    id: int


class TaskStatusResponse(BaseModel):
    status: str


class TaskResultResponse(BaseModel):
    result: str
