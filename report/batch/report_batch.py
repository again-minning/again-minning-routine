from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from base.utils.collection import to_dict
from base.utils.time import get_now
from config.settings import settings
from report.schema import CreateReportSchema, RoutineElement, RoutineResultElement, Report


async def create_weekly_report(mongo_db: AsyncIOMotorClient, request: CreateReportSchema):
    res = []
    routines = to_dict(request.routines, 'id')
    routine_results_data = to_dict(request.routine_results, 'routine_id')
    await _skipped_empty_result_routines(routine_results_data, routines)
    _none = 0
    _try = 0
    _done = 0
    random_key = None
    for key in routines.keys():
        random_key = key
        routine = routines[key][0]
        routine_results = routine_results_data[key]
        ele = []
        for routine_result in routine_results:
            if routine_result.result.value == 'NOT':
                _none += 1
            elif routine_result.result.value == 'TRY':
                _try += 1
            elif routine_result.result.value == 'DONE':
                _done += 1
            else:
                pass
            ele.append(RoutineResultElement(date=routine_result.date, result=routine_result.result.value))
        res.append(
            RoutineElement(
                routine_id=routine.id, title=routine.title,
                category=routine.category,
                results=ele)
        )
    if random_key:
        report = Report(
            account_id=routines[random_key][0].account_id,
            achievement_rate=Report.calculate_achievement_rate(_done=_done, _try=_try, _none=_none),
            done_count=_done, try_count=_try, none_count=_none,
            routine_results=res,
            created_at=str(get_now())
        )
        db_report = jsonable_encoder(report)
        new_report = await mongo_db[settings.DB_NAME]['reports'].insert_one(db_report)
        report_id = await mongo_db[settings.DB_NAME]['reports'].find_one({'_id': new_report.inserted_id})
        return report_id


async def _skipped_empty_result_routines(routine_results_data, routines):
    skipped_make_report_for_routines = routines.keys() - routine_results_data.keys()
    for key in skipped_make_report_for_routines:
        del routines[key]
