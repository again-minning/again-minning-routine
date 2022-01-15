from routine.models import routine, routineDay, routineResult
from retrospect.models import retrospect, snapshot
from base.database.database import engine
from base.database.database import Base
from routine.models.routine import Routine, RoutineDay, RoutineResult
from retrospect.models.retrospect import Retrospect
from retrospect.models.snapshot import Snapshot
# 로컬 에서만 할 것!
Base.metadata.drop_all(bind=engine)

models = [Routine, RoutineDay, RoutineResult, Retrospect, Snapshot]
# 생성
CONNECTION = (
    routine.Base.metadata.create_all(bind=engine),
    routineDay.Base.metadata.create_all(bind=engine),
    retrospect.Base.metadata.create_all(bind=engine),
    snapshot.Base.metadata.create_all(bind=engine),
    routineResult.Base.metadata.create_all(bind=engine)
)
