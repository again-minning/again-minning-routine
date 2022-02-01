from base.utils.constants import ConnectionMode
from routine.models import routine, routineDay, routineResult
from retrospect.models import retrospect, snapshot
from base.database.database import engine
from base.database.database import Base
from routine.models.routine import Routine, RoutineDay, RoutineResult
from retrospect.models.retrospect import Retrospect
from retrospect.models.snapshot import Snapshot
from config.settings import settings
models = [Routine, RoutineDay, RoutineResult, Retrospect, Snapshot]


def CONNECTION():
    routine.Base.metadata.create_all(bind=engine)
    routineDay.Base.metadata.create_all(bind=engine)
    retrospect.Base.metadata.create_all(bind=engine)
    snapshot.Base.metadata.create_all(bind=engine)
    routineResult.Base.metadata.create_all(bind=engine)


class Connection:
    def __init__(self, ddl_mode: ConnectionMode = ConnectionMode.CREATE):
        self.ddl_mode = ddl_mode
        if settings.APP_ENV == 'test':
            self.ddl_mode = ConnectionMode.CREATE
        self.__execute()

    def __execute(self):
        if self.ddl_mode == ConnectionMode.NONE:
            print('===============NONE==================')
            return
        if self.ddl_mode == ConnectionMode.UPDATE:
            print('===============UPDATE==================')
            CONNECTION()
            return
        if self.ddl_mode == ConnectionMode.CREATE:
            print('===============CREATE==================')
            Base.metadata.drop_all(bind=engine)
            CONNECTION()
            return
