import freezegun
from assertpy import assert_that
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.utils.time import convert_str2time, get_now, get_last_week_about, get_start_datetime, get_end_datetime, convert_str2datetime
from routine.constants.category import Category
from routine.constants.result import Result
from routine.constants.week import Week
from test.conftest import maintain_idempotent
from routine.models.routine import Routine
from routine.repository.routine_batch_repository import get_routine_count, get_routine_pagination, get_routine_results_search_in

routines_router_url = '/api/v1/routines'
routines_batch_router_url = '/api/v1/batch-routines'


@maintain_idempotent
def test_루틴_전체_갯수_가져오기(db: Session, client: TestClient):
    res = []
    for i in range(10):
        res.append(
            Routine(
                title=f'글{i}', category=Category.SELF,
                goal=f'목표{i}', is_alarm=True,
                start_time=convert_str2time('10:00:00'),
                account_id=1)
        )
    db.add_all(res)
    db.commit()
    count = get_routine_count(db=db)
    assert_that(count).is_equal_to(10)


@maintain_idempotent
def test_루틴_전체_갯수_가져오기_e2e(db: Session, client: TestClient):
    res = []
    for i in range(10):
        res.append(
            Routine(
                title=f'글{i}', category=Category.SELF,
                goal=f'목표{i}', is_alarm=True,
                start_time=convert_str2time('10:00:00'),
                account_id=1)
        )
    db.add_all(res)
    db.commit()
    response = client.get(
        f'{routines_batch_router_url}/count'
    )
    assert_that(response.status_code).is_equal_to(200)
    data = response.json()['data']
    assert_that(data['count']).is_equal_to(10)


@maintain_idempotent
def test_루틴_페이지네이션(db: Session, client: TestClient):
    res = []
    for i in range(10):
        res.append(
            Routine(
                title=f'글{i}', category=Category.SELF,
                goal=f'목표{i}', is_alarm=True,
                start_time=convert_str2time('10:00:00'),
                account_id=1)
        )
    db.add_all(res)
    db.commit()
    limit = 5
    offset = 0
    routines = get_routine_pagination(db=db, limit=limit, offset=offset)
    results = []
    for routine in routines:
        results.append(routine)
    assert_that(len(results)).is_equal_to(5)
    result = results[0]
    assert_that(result).contains(Category.SELF)


@maintain_idempotent
def test_루틴_페이지네이션_e2e(db: Session, client: TestClient):
    res = []
    for i in range(10):
        res.append(
            Routine(
                title=f'글{i}', category=Category.SELF,
                goal=f'목표{i}', is_alarm=True,
                start_time=convert_str2time('10:00:00'),
                account_id=1)
        )
    db.add_all(res)
    db.commit()
    limit = 5
    offset = 0
    response = client.get(
        f'{routines_batch_router_url}?limit={limit}&offset={offset}'
    )
    assert_that(response.status_code).is_equal_to(200)
    data = response.json()['data']
    assert_that(len(data)).is_equal_to(5)


@maintain_idempotent
def test_루틴결과_루틴아이디를_통해_조회_and_e2e(db: Session, client: TestClient):
    with freezegun.freeze_time('2022-02-07'):  # 월요일
        for i in range(10):
            data = {
                'title': f'글{i}',
                'category': 1,
                'goal': f'목표{i}',
                'is_alarm': True,
                'start_time': '10:00:00',
                'days': ['MON', 'WED', 'SAT']
            }
            client.post(
                f'{routines_router_url}',
                json=data,
                headers={'account': '1'}
            )
        limit = 5
        offset = 0
        routines = get_routine_pagination(db=db, limit=limit, offset=offset)
        routine_ids = []
        for routine in routines:
            routine_ids.append(routine.id)

    with freezegun.freeze_time('2022-02-07'):  # 월요일
        now = get_now()
        data = {
            'result': 'DONE'
        }
        client.post(
            f'{routines_router_url}/{routine_ids[0]}/check-result?date={now.strftime("%Y-%m-%d")}',
            json=data,
            headers={'account': '1'}
        )
        client.post(
            f'{routines_router_url}/{routine_ids[1]}/check-result?date={now.strftime("%Y-%m-%d")}',
            json=data,
            headers={'account': '1'}
        )

    with freezegun.freeze_time('2022-02-09'):  # 수요일
        now = get_now()
        data = {
            'result': 'DONE'
        }
        client.post(
            f'{routines_router_url}/{routine_ids[2]}/check-result?date={now.strftime("%Y-%m-%d")}',
            json=data,
            headers={'account': '1'}
        )
        client.post(
            f'{routines_router_url}/{routine_ids[3]}/check-result?date={now.strftime("%Y-%m-%d")}',
            json=data,
            headers={'account': '1'}
        )
    with freezegun.freeze_time('2022-02-12'):  # 토요일
        now = get_now()
        data = {
            'result': 'DONE'
        }
        client.post(
            f'{routines_router_url}/{routine_ids[4]}/check-result?date={now.strftime("%Y-%m-%d")}',
            json=data,
            headers={'account': '1'}
        )
    with freezegun.freeze_time('2022-02-14'):  # 월요일(주간 리포트 생성 요일)
        start_date = get_start_datetime(get_last_week_about(date=get_now(), week=Week.MON))
        end_date = get_end_datetime(get_last_week_about(date=get_now(), week=Week.SUN))
        results = get_routine_results_search_in(db=db, start_date=start_date, end_date=end_date, routine_ids=routine_ids)
        assert_that(len(results)).is_equal_to(8)
        for i in range(5):
            assert_that(results[i].yymmdd).is_equal_to(convert_str2datetime('2022-02-07'))
            if results[i].routine_id in (routine_ids[0], routine_ids[1]):
                assert_that(results[i].result).is_equal_to(Result.DONE)
            else:
                assert_that(results[i].result).is_equal_to(Result.NOT)
        for i in range(5, 7):
            assert_that(results[i].yymmdd).is_equal_to(convert_str2datetime('2022-02-09'))
            assert_that(results[i].result).is_equal_to(Result.DONE)
        assert_that(results[7].yymmdd).is_equal_to(convert_str2datetime('2022-02-12'))
        assert_that(results[7].result).is_equal_to(Result.DONE)
        response = client.get(
            f'{routines_batch_router_url}/results?start-date={start_date}&end-date={end_date}'
            f'&routine-ids={routine_ids[0]}&routine-ids={routine_ids[1]}&routine-ids={routine_ids[2]}&routine-ids={routine_ids[3]}&routine-ids={routine_ids[4]}'
        )
        results = response.json()['data']
        assert_that(len(results)).is_equal_to(8)
        pass
