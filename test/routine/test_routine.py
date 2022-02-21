import datetime
from unittest.mock import patch

import freezegun
from assertpy import assert_that
from sqlalchemy import desc, and_
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.constants.base_message import USER_INFO_NOT_EQUAL
from test.utils import get_now_date
from base.utils.constants import HttpStatus
from base.utils.time import get_now, convert_str2datetime, convert_str2date
from routine.constants.result import Result
from routine.constants.routine_message import ROUTINE_CREATE_MESSAGE, ROUTINE_FIELD_TITLE_ERROR_MESSAGE, ROUTINE_FIELD_DAYS_ERROR_MESSAGE, ROUTINE_GET_MESSAGE, ROUTINE_RESULTS_UPDATE_MESSAGE, \
    ROUTINE_NO_DATA_RESPONSE, ROUTINE_DELETE_RESPONSE, ROUTINE_RESULT_CANCEL_MESSAGE
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from routine.service.routine_service import patch_routine_detail, update_or_create_routine_result, create_routine
from routine.schemas import RoutineCreateRequest, RoutineResultUpdateRequest
from test.conftest import maintain_idempotent

routines_router_url = '/api/v1/routines'


@maintain_idempotent
def test_루틴_생성_성공했을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_CREATE_MESSAGE)
    assert_that(body['success']).is_true()


@freezegun.freeze_time('2022-01-27')  # 목요일
@maintain_idempotent
def test_루틴_생성이_해당_수행하는_요일과_맞을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'time_test',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['THU']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    assert_that(response.status_code).is_equal_to(200)
    # select routine
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    routine_id = routine.id
    assert_that(routine.title).is_equal_to(data['title'])
    assert_that(routine.category.value).is_equal_to(data['category'])
    assert_that(routine.goal).is_equal_to(data['goal'])
    assert_that(routine.account_id).is_equal_to(1)
    assert_that(routine.is_alarm).is_true()
    # select routine_day
    routine_day = db.query(RoutineDay).filter(RoutineDay.routine_id == routine_id).all()
    assert_that(len(routine_day)).is_equal_to(1)
    # select routine_results
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    assert_that(routine_results[0].result).is_equal_to('NOT')


@freezegun.freeze_time('2022-01-27')  # 목요일
@maintain_idempotent
def test_루틴_생성이_해당_수행하는_요일과_맞지_않을때(db: Session, client: TestClient):
    days = ['FRI', 'SAT', 'SUN']
    # given
    data = {
        'title': 'time_test',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': days
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    assert_that(response.status_code).is_equal_to(200)
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    routine_id = routine.id
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    assert_that(len(routine_results)).is_zero()


@maintain_idempotent
def test_루틴_생성_루틴_이름_공백일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': '',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    method = result['method']
    path = result['path']
    detail = result['detail']
    detail = detail[0]
    msg = detail['msg']
    error_type = detail['type']
    body = result['body']
    assert_that(method).is_equal_to('POST')
    assert_that(path).is_equal_to(f'{routines_router_url}')
    assert_that(msg).is_equal_to(ROUTINE_FIELD_TITLE_ERROR_MESSAGE)
    assert_that(error_type).is_equal_to('value_error')
    assert_that(body).is_equal_to(data)


@maintain_idempotent
def test_루틴_생성_카테고리_선택하지_않을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    method = result['method']
    path = result['path']
    detail = result['detail']
    detail = detail[0]
    msg = detail['msg']
    error_type = detail['type']
    body = result['body']
    assert_that(method).is_equal_to('POST')
    assert_that(path).is_equal_to(f'{routines_router_url}')
    assert_that(msg).is_equal_to('field required')
    assert_that(error_type).is_equal_to('value_error.missing')
    assert_that(body).is_equal_to(data)


@maintain_idempotent
def test_루틴_생성_요일_값_전달받지_못할_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00'
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    method = result['method']
    path = result['path']
    detail = result['detail']
    detail = detail[0]
    msg = detail['msg']
    error_type = detail['type']
    body = result['body']
    assert_that(method).is_equal_to('POST')
    assert_that(path).is_equal_to(f'{routines_router_url}')
    assert_that(msg).is_equal_to(ROUTINE_FIELD_DAYS_ERROR_MESSAGE)
    assert_that(error_type).is_equal_to('value_error')
    assert_that(body).is_equal_to(data)


@maintain_idempotent
def test_루틴_생성_알람보내기값이_null일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'is_alarm',
        'category': 'SELF',
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_CREATE_MESSAGE)
    assert_that(body['success']).is_true()


@maintain_idempotent
def test_루틴_전체조회(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'category': 'SELF',
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    today = get_now()
    # when
    response = client.get(
        f'{routines_router_url}/account?today={today.strftime("%Y-%m-%d")}',
        headers={'account': '1'}
    )
    result = response.json()
    message = result['message']
    body = result['data'][0]
    # then
    assert_that(message['status']).is_equal_to('ROUTINE_LIST_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_GET_MESSAGE)
    assert_that(body['title']).is_equal_to(data['title'])
    assert_that(body['goal']).is_equal_to(data['goal'])
    assert_that(body['start_time']).is_equal_to(data['start_time'])
    assert_that(body['result']).is_equal_to('NOT')


@maintain_idempotent
def test_루틴_조회_이때_루틴결과값이_여러개이지만_하나만_가져오는지(db: Session, client: TestClient):
    now_weekday = datetime.datetime.now().weekday()
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days.remove(Week.get_weekday(now_weekday))
    data = {
        'title': 'yes',
        'category': 'SELF',
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': days
    }
    client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    from datetime import timedelta
    today = get_now()
    tomorrow = today + timedelta(days=1)
    # when
    response = client.get(
        f'{routines_router_url}/account?today={tomorrow.strftime("%Y-%m-%d")}',
        headers={'account': '1'}
    )
    result = response.json()
    body = result['data'][0]
    assert_that(body['result']).is_equal_to('NOT')
    routine_id = body['id']
    with patch('base.utils.time.get_now') as now:
        now.return_value = convert_str2datetime(tomorrow.strftime("%Y-%m-%d"))
        routine_result_data = {
            'result': 'DONE'
        }
        response = client.post(
            f'{routines_router_url}/{routine_id}/check-result?date={tomorrow.strftime("%Y-%m-%d")}',
            json=routine_result_data,
            headers={'account': '1'}
        )
    result = response.json()
    message = result['message']
    body = result['data']
    # then
    assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_OK.value)
    assert_that(message['msg']).is_equal_to(ROUTINE_RESULTS_UPDATE_MESSAGE)
    assert_that(body['success']).is_true()

    response = client.get(
        f'{routines_router_url}/account?today={tomorrow.strftime("%Y-%m-%d")}',
        headers={'account': '1'}
    )
    result = response.json()
    body = result['data'][0]
    assert_that(body['result']).is_equal_to('DONE')


@maintain_idempotent
def test_루틴_값_수정하는데_요일일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'category': 'SELF',
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    routine = db.query(Routine).filter(and_(Routine.title == data['title'], Routine.account_id == 1)).first()
    patch_data = {
        'title': 'bye',
        'category': 'SELF',
        'goal': 'say-good-bye',
        'start_time': '11:00:00',
        'days': ['MON', 'WED', 'THU']
    }
    # when
    client.patch(
        f'{routines_router_url}/{routine.id}',
        json=patch_data,
        headers={'account': '1'}
    )
    # then
    days = db.query(RoutineDay.day).filter(RoutineDay.routine_id == routine.id).all()
    result = []
    for day in days:
        result.append(day[0].value)
    result.sort()
    assert_that(result).is_equal_to(sorted(patch_data['days']))


@maintain_idempotent
def test_루틴_값_수정하는데_요일이_아닌_다른_것(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'category': 'SELF',
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    routine: Routine = db.query(Routine).filter(and_(Routine.title == data['title'], Routine.account_id == 1)).first()
    patch_data = RoutineCreateRequest(
        title='bye',
        category='SELF', goal='say-good-bye',
        start_time='11:00:00', days=['FRI', 'SAT', 'SUN']
    )
    # when
    patch_routine_detail(db=db, routine_id=routine.id, request=patch_data, account=1)
    # then
    response = client.get(
        f'{routines_router_url}/{routine.id}',
        headers={'account': '1'}
    )
    result = response.json()
    result_data = result['data']
    assert_that(result_data['title']).is_equal_to(patch_data.title)
    assert_that(result_data['goal']).is_equal_to(patch_data.goal)
    assert_that(str(result_data['start_time'])).is_equal_to(patch_data.start_time)


@freezegun.freeze_time('2022-01-27')  # 목요일
@maintain_idempotent
def test_루틴_수행여부_값_저장_오늘이_수행하는_날일_때(db: Session, client: TestClient):
    # given
    create = {
        'title': 'wake_up',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['THU']
    }
    # when
    client.post(
        f'{routines_router_url}',
        json=create,
        headers={'account': '1'}
    )
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)
    routine_data = {
        'result': 'DONE'
    }
    # when
    response = client.post(
        f'{routines_router_url}/{routine.id}/check-result?date={date.strftime("%Y-%m-%d")}',
        json=routine_data,
        headers={'account': '1'}
    )
    # then
    result = response.json()
    message = result['message']
    data = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_RESULTS_UPDATE_MESSAGE)
    assert_that(data['success']).is_true()
    routine_result = db.query(RoutineResult).filter(and_(RoutineResult.routine_id == routine.id, RoutineResult.yymmdd == date)).first()
    assert_that(routine_result.result).is_equal_to(Result.DONE)


@freezegun.freeze_time('2022-01-27')  # 목요일
@maintain_idempotent
def test_루틴_결과_체크하는데_Default인_경우(db: Session, client: TestClient):
    # given
    days = ['MON', 'TUE', 'WED', 'FRI', 'SAT', 'SUN']
    create = {
        'title': 'wake_up',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': days
    }
    # when
    client.post(
        f'{routines_router_url}',
        json=create,
        headers={'account': '1'}
    )
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)
    routine_data = {
        'result': 'DONE'
    }
    # when
    response = client.post(
        f'{routines_router_url}/{routine.id}/check-result?date={date.strftime("%Y-%m-%d")}',
        json=routine_data,
        headers={'account': '1'}
    )
    # then
    assert_that(response.status_code).is_equal_to(200)
    routine_result = db.query(RoutineResult).filter(and_(RoutineResult.routine_id == routine.id, RoutineResult.yymmdd == date)).first()
    assert_that(routine_result).is_not_none()
    assert_that(routine_result.result).is_equal_to(Result.DONE)
    routine_results = db.query(RoutineResult).all()
    assert_that(len(routine_results)).is_equal_to(1)


@maintain_idempotent
def test_루틴_디테일_조회(db: Session, client: TestClient):
    # given
    data = {
        'title': 'time_test',
        'category': 'SELF',
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data,
        headers={'account': '1'}
    )
    assert_that(response.status_code).is_equal_to(200)
    routine: Routine = db.query(Routine).filter(Routine.title == data['title']).first()
    response = client.get(
        f'{routines_router_url}/{routine.id}',
        headers={'account': '1'}
    )
    result = response.json()
    message = result['message']
    body = result['data']
    # then
    assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_DETAIL_OK.value)
    assert_that(message['msg']).is_equal_to(ROUTINE_GET_MESSAGE)
    assert_that(body['id']).is_equal_to(routine.id)
    assert_that(body['title']).is_equal_to(data['title'])
    assert_that(body['category']).is_equal_to(data['category'])
    assert_that(body['goal']).is_equal_to(data['goal'])
    assert_that(len(body['days'])).is_equal_to(7)


@maintain_idempotent
def test_루틴_수행여부_취소(db: Session, client: TestClient):
    # given
    routine_data = RoutineCreateRequest(
        title='time_test', category='SELF',
        goal='daily', is_alarm=True,
        start_time='10:00:00',
        days=[Week.MON, Week.TUE, Week.WED, Week.THU, Week.FRI, Week.SAT, Week.SUN]
    )
    create_routine(db=db, routine=routine_data, account=1)
    # when
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)

    update_or_create_routine_result(db=db, routine_id=routine.id, date=date.strftime("%Y-%m-%d"), reqeust=RoutineResultUpdateRequest(result=Result.DONE))
    routine_result: RoutineResult = db.query(RoutineResult).first()
    assert_that(routine_result.result).is_equal_to(Result.DONE)

    response = client.patch(
        f'{routines_router_url}/cancel/{routine.id}?date={date.strftime("%Y-%m-%d")}',
        headers={'account': '1'}
    )
    # then
    response_json = response.json()
    message = response_json['message']
    body = response_json['data']
    assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_PATCH_OK.value)
    assert_that(message['msg']).is_equal_to(ROUTINE_RESULT_CANCEL_MESSAGE)
    assert_that(body['success']).is_true()


@maintain_idempotent
def test_루틴_수행여부_취소하는데_유저아이디_불일치(db: Session, client: TestClient):
    # given
    routine_data = RoutineCreateRequest(
        title='time_test', category='SELF',
        goal='daily', is_alarm=True,
        start_time='10:00:00',
        days=[Week.MON, Week.TUE, Week.WED, Week.THU, Week.FRI, Week.SAT, Week.SUN]
    )
    create_routine(db=db, routine=routine_data, account=1)
    # when
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)

    update_or_create_routine_result(db=db, routine_id=routine.id, date=date.strftime("%Y-%m-%d"), reqeust=RoutineResultUpdateRequest(result=Result.DONE))
    routine_result: RoutineResult = db.query(RoutineResult).first()
    assert_that(routine_result.result).is_equal_to(Result.DONE)

    response = client.patch(
        f'{routines_router_url}/cancel/{routine.id}?date={date.strftime("%Y-%m-%d")}',
        headers={'account': '2'}
    )
    assert_that(response.status_code).is_equal_to(400)
    result = response.json()
    assert_that(result['body']).is_equal_to(USER_INFO_NOT_EQUAL)


@maintain_idempotent
def test_존재하지_않는_아이디_조회했을_때(db: Session, client: TestClient):
    response = client.get(
        f'{routines_router_url}/123',
        headers={'account': '1'}
    )
    result = response.json()
    assert_that(result['path']).is_equal_to(f'{routines_router_url}/123')
    assert_that(result['body']).is_equal_to(ROUTINE_NO_DATA_RESPONSE)


@maintain_idempotent
def test_2일이상_된_루틴결과_수정했을_때(db: Session, client: TestClient):
    with freezegun.freeze_time('2022-01-28'):
        routine_data = RoutineCreateRequest(
            title='time_test', category='SELF',
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.MON, Week.TUE, Week.WED, Week.THU, Week.FRI, Week.SAT, Week.SUN]
        )
        create_routine(db=db, routine=routine_data, account=1)

    routine = db.query(Routine).first()
    with freezegun.freeze_time('2022-01-31'):   # 3일 경과
        date = get_now_date()
        routine_data = {
            'result': 'YET'
        }
        # when
        response = client.post(
            f'{routines_router_url}/{routine.id}/check-result?date={date.strftime("%Y-%m-%d")}',
            json=routine_data,
            headers={'account': '1'}
        )
        # then
        assert_that(response.status_code).is_equal_to(400)


@maintain_idempotent
def test_3일이상_된_루틴결과_수정했을_때(db: Session, client: TestClient):
    with freezegun.freeze_time('2022-01-28'):
        routine_data = RoutineCreateRequest(
            title='time_test', category='SELF',
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.MON, Week.TUE, Week.WED, Week.THU, Week.FRI, Week.SAT, Week.SUN]
        )
        create_routine(db=db, routine=routine_data, account=1)

    routine = db.query(Routine).first()
    with freezegun.freeze_time('2022-01-30'):   # 2일 경과
        date = get_now_date()
        routine_data = {
            'result': 'DONE'
        }
        # when
        response = client.post(
            f'{routines_router_url}/{routine.id}/check-result?date={date.strftime("%Y-%m-%d")}',
            json=routine_data,
            headers={'account': '1'}
        )
        # then
        assert_that(response.status_code).is_equal_to(200)


@maintain_idempotent
def test_수행여부_취소하고자_하는데_해당_아이디가_없을_때(db: Session, client: TestClient):
    response = client.patch(
        f'{routines_router_url}/cancel/123?date=2022-01-28',
        headers={'account': '1'}
    )
    assert_that(response.status_code).is_equal_to(400)
    pass


@maintain_idempotent
def test_루틴_삭제(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-30'):   # 일요일
        routine_data = RoutineCreateRequest(
            title='time_test', category='SELF',
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.SUN]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
    # when
        response = client.delete(
            f'{routines_router_url}/{routine.id}',
            headers={'account': '1'}
        )
        result = response.json()
    # then
        message = result['message']
        assert_that(message['msg']).is_equal_to(ROUTINE_DELETE_RESPONSE)
        assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_DELETE_OK.value)


@maintain_idempotent
def test_루틴_순서_변경(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-30'):   # 일요일
        routine_data = RoutineCreateRequest(
            title='첫째', category='SELF',
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.SUN]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine_data = RoutineCreateRequest(
            title='둘째', category='HEALTH',
            goal='second', is_alarm=True,
            start_time='09:00:00',
            days=[Week.SUN]
        )
        create_routine(db=db, routine=routine_data, account=1)
        change_sequence = {
            'routine_sequences': [
                {
                    'routine_id': 2,
                    'sequence': 1
                },
                {
                    'routine_id': 1,
                    'sequence': 2
                }
            ]
        }
    # when
        date = '2022-01-30'
        response = client.patch(
            f'{routines_router_url}/days/sequence?date={date}',
            json=change_sequence,
            headers={'account': '1'}
        )
    # then
        assert_that(response.status_code).is_equal_to(200)
        routine_id_and_sequences = db.query(RoutineDay.routine_id, RoutineDay.sequence).all()
        assert_that(sorted(routine_id_and_sequences)).is_equal_to([(1, 2), (2, 1)])


@maintain_idempotent
def test_루틴디테일_유저아이디가_일치하지_않을_때(db: Session, client: TestClient):
    routine_data = RoutineCreateRequest(
        title='첫째', category='SELF',
        goal='daily', is_alarm=True,
        start_time='10:00:00',
        days=[Week.SUN]
    )
    create_routine(db=db, routine=routine_data, account=1)
    routine = db.query(Routine).first()
    response = client.get(
        f'{routines_router_url}/{routine.id}',
        headers={'account': '2'}
    )
    assert_that(response.status_code).is_equal_to(400)
    result = response.json()
    message = result['body']
    assert_that(message).is_equal_to(ROUTINE_NO_DATA_RESPONSE)
