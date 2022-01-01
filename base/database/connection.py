from routine.models import routine, routineDay
from base.database.database import engine
from base.database.database import Base

# 로컬 에서만 할 것!
Base.metadata.drop_all(bind=engine)
# 생성
CONNECTION = (
    routine.Base.metadata.create_all(bind=engine),
    routineDay.Base.metadata.create_all(bind=engine)
)
