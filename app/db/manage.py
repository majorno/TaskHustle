from app.models.kind import Kind, TaskKind
from app.models.status import Status, TaskStatus
from app.db.core import Base, engine


async def init_db(session) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session.add(Kind(id=int(TaskKind.REVERSE), name='reverse'))
    session.add(Kind(id=int(TaskKind.SWAP), name='swap'))
    session.add(Kind(id=int(TaskKind.REPEAT), name='repeat'))

    session.add(Status(id=int(TaskStatus.PENDING), name='Pending'))
    session.add(Status(id=int(TaskStatus.PROCESSING), name='Processing'))
    session.add(Status(id=int(TaskStatus.COMPLETE), name='Complete'))

    await session.commit()
