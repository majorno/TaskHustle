import asyncio
from sqlalchemy.future import select
from app.models.task import Task
from app.models.kind import TaskKind
from app.models.status import TaskStatus


class Worker:
    def __init__(self, session):
        self.running = True
        self.session = session
        self.executor_map = {int(TaskKind.REVERSE): self.reverse,
                             int(TaskKind.SWAP): self.swap,
                             int(TaskKind.REPEAT): self.repeat}

    async def run(self) -> None:
        while self.running:
            query = await self.session.execute(select(Task).filter_by(status_id=TaskStatus.PENDING).order_by(Task.id))
            records = query.scalars().all()

            if not records:
                await asyncio.sleep(1)
                continue

            for record in records:
                record.status_id = int(TaskStatus.PROCESSING)
                await self.session.commit()

                if record.kind_id in self.executor_map:
                    executor = self.executor_map[record.kind_id]
                    record.result = await executor(record.data)

                record.status_id = int(TaskStatus.COMPLETE)
                await self.session.commit()

    def stop(self) -> None:
        self.running = False

    @staticmethod
    async def reverse(data: str) -> str:
        await asyncio.sleep(2)
        return data[::-1]

    @staticmethod
    async def swap(data: str) -> str:
        await asyncio.sleep(5)
        return ''.join([data[x:x + 2][::-1] for x in range(0, len(data), 2)])

    @staticmethod
    async def repeat(data: str) -> str:
        await asyncio.sleep(7)
        return ''.join([data[x] * (x + 1) for x in range(0, len(data))])
