from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from base.utils.collection import to_dict
from base.utils.time import get_now, get_start_datetime
from config.settings import settings
from report.collections import Collections
from report.schema import CreateReportSchema, RoutineElement, RoutineResultElement, Report, MonthlyReport


async def create_monthly_report(mongo_db: AsyncIOMotorClient, account_id: int):
    weekly_report_list = mongo_db[settings.DB_NAME]['reports'].find({'account_id': account_id}).sort([('created_at', -1)])
    weekly_achievement_rate = []
    category_detail, category_routine_count = await __default_category_settings()
    for weekly_report in await weekly_report_list.to_list(length=4):
        weekly_achievement_rate.append(weekly_report['achievement_rate'])
        for routine_result in weekly_report['routine_results']:
            category = routine_result['category']
            routine_id = str(routine_result['routine_id'])

            detail_category = category_detail[category]
            detail = await __counting_routine_results(routine_id, routine_result, detail_category)
            category_routine_count[category].add(routine_id)
            category_detail[category][routine_id] = detail
    weekly_achievement_rate = await __resizing_weekly_achievement_rate(weekly_achievement_rate)
    await __calculating_category_routines_count(category_routine_count)
    report = MonthlyReport(
        account_id=account_id, weekly_achievement_rate=weekly_achievement_rate,
        category_routine_count=category_routine_count, category_detail=category_detail,
        created_at=get_start_datetime(get_now())
    )
    db_report = jsonable_encoder(report)
    new_report = await mongo_db[settings.DB_NAME][Collections.MONTHLY_REPORT.value].insert_one(db_report)
    find_report = await mongo_db[settings.DB_NAME][Collections.MONTHLY_REPORT.value].find_one({'_id': new_report.inserted_id})
    return find_report


async def __default_category_settings():
    category_routine_count = {
        'MIRACLE': set(),
        'SELF': set(),
        'HEALTH': set(),
        'DAILY': set(),
        'ETC': set()
    }
    category_detail = {
        'MIRACLE': {},
        'SELF': {},
        'HEALTH': {},
        'DAILY': {},
        'ETC': {}
    }
    return category_detail, category_routine_count


async def __counting_routine_results(routine_id, routine_result, detail_category):
    default_schema = {
        'title': routine_result['title'],
        'done_count': 0,
        'try_count': 0,
        'not_count': 0
    }
    detail: dict = detail_category.get(routine_id, default_schema)
    data = {
        'done_count': 0,
        'try_count': 0,
        'not_count': 0
    }
    for result in routine_result['results']:
        keyword: str = result['result'].lower()
        data[f'{keyword}_count'] += 1
    for k, v in data.items():
        detail[k] += v
    return detail


async def __resizing_weekly_achievement_rate(weekly_achievement_rate):
    current_size = len(weekly_achievement_rate)
    weekly_achievement_rate = [0.0] * (4 - current_size) + weekly_achievement_rate
    return weekly_achievement_rate


async def __calculating_category_routines_count(category_routine_count):
    total = 0
    each_category_percent = {}
    for k, v in category_routine_count.items():
        each_category_percent[k] = len(v)
        total += len(v)
    for k, v in category_routine_count.items():
        category_routine_count[k] = each_category_percent[k]


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
            done_count=_done, try_count=_try, not_count=_none,
            routine_results=res,
            created_at=get_start_datetime(get_now())
        )
        db_report = jsonable_encoder(report)
        new_report = await mongo_db[settings.DB_NAME][Collections.REPORT.value].insert_one(db_report)
        find_report = await mongo_db[settings.DB_NAME][Collections.REPORT.value].find_one({'_id': new_report.inserted_id})
        return find_report


async def _skipped_empty_result_routines(routine_results_data, routines):
    skipped_make_report_for_routines = routines.keys() - routine_results_data.keys()
    for key in skipped_make_report_for_routines:
        del routines[key]
