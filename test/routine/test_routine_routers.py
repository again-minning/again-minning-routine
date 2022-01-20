import datetime
from unittest.mock import patch

from assertpy import assert_that
from sqlalchemy import desc, and_
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.utils.constants import HttpStatus
from base.utils.time import get_now, convert_str2datetime, convert_str2date
from routine.constants.result import Result
from routine.constants.routine_message import ROUTINE_CREATE_MESSAGE, ROUTINE_GET_MESSAGE, ROUTINE_RESULTS_UPDATE_MESSAGE, ROUTINE_FIELD_DAYS_ERROR_MESSAGE, ROUTINE_FIELD_TITLE_ERROR_MESSAGE
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from test.conftest import complex_transaction

routines_router_url = '/api/v1/routines'


@complex_transaction
def test_루틴_생성_성공했을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_CREATE_MESSAGE)
    assert_that(body['success']).is_true()


@complex_transaction
def test_루틴_생성이_해당_수행하는_요일과_맞을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'time_test',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
    )
    assert_that(response.status_code).is_equal_to(200)
    # select routine
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    routine_id = routine.id
    assert_that(routine.title).is_equal_to(data['title'])
    assert_that(routine.category.value).is_equal_to(data['category'])
    assert_that(routine.goal).is_equal_to(data['goal'])
    assert_that(routine.account_id).is_equal_to(data['account_id'])
    assert_that(routine.is_alarm).is_true()
    # select routine_day
    routine_day = db.query(RoutineDay).filter(RoutineDay.routine_id == routine_id).all()
    assert_that(len(routine_day)).is_equal_to(7)
    # select routine_results
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    assert_that(routine_results[0].result).is_equal_to('NOT')


@complex_transaction
def test_루틴_생성이_해당_수행하는_요일과_맞지_않을때(db: Session, client: TestClient):
    now_weekday = datetime.datetime.now().weekday()
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days.remove(Week.get_weekday(now_weekday))
    # given
    data = {
        'title': 'time_test',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': days
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
    )
    assert_that(response.status_code).is_equal_to(200)
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    routine_id = routine.id
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    assert_that(len(routine_results)).is_zero()


def test_루틴_생성_루틴_이름_공백일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': '',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
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


@complex_transaction
def test_루틴_생성_카테고리_선택하지_않을_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'account_id': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
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


@complex_transaction
def test_루틴_생성_요일_값_전달받지_못할_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'wake_up',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00'
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
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


@complex_transaction
def test_루틴_생성_알람보내기값이_null일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'is_alarm',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['MON', 'WED', 'FRI']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to(ROUTINE_CREATE_MESSAGE)
    assert_that(body['success']).is_true()


@complex_transaction
def test_루틴_전체조회(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data
    )
    account_id = 1
    today = get_now()
    # when
    response = client.get(
        f'{routines_router_url}/account/{account_id}?today={today.strftime("%Y-%m-%d")}',
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


@complex_transaction
def test_루틴_조회_이때_루틴결과값이_여러개이지만_하나만_가져오는지(db: Session, client: TestClient):
    now_weekday = datetime.datetime.now().weekday()
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days.remove(Week.get_weekday(now_weekday))
    data = {
        'title': 'yes',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': days
    }
    client.post(
        f'{routines_router_url}',
        json=data
    )
    account_id = 1
    from datetime import timedelta
    today = get_now()
    tomorrow = today + timedelta(days=1)
    # when
    response = client.get(
        f'{routines_router_url}/account/{account_id}?today={tomorrow.strftime("%Y-%m-%d")}',
    )
    result = response.json()
    body = result['data'][0]
    assert_that(body['result']).is_equal_to('NOT')
    routine_id = body['id']
    with patch('base.utils.time.get_now') as now:
        now.return_value = convert_str2datetime(tomorrow.strftime("%Y-%m-%d"))
        routine_result_data = {
            'result': 'DONE',
            'weekday': Week.get_weekday(tomorrow.weekday()),
            'date': tomorrow.strftime("%Y-%m-%d")
        }
        response = client.post(
            f'{routines_router_url}/{routine_id}/check-result',
            json=routine_result_data
        )
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_OK.value)
    assert_that(message['msg']).is_equal_to(ROUTINE_RESULTS_UPDATE_MESSAGE)
    assert_that(body['success']).is_true()

    response = client.get(
        f'{routines_router_url}/account/{account_id}?today={tomorrow.strftime("%Y-%m-%d")}',
    )
    result = response.json()
    body = result['data'][0]
    assert_that(body['result']).is_equal_to('DONE')
    pass


def test_루틴_값_수정하는데_요일일_때(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data
    )
    routine = db.query(Routine).filter(and_(Routine.title == data['title'], Routine.account_id == data['account_id'])).first()
    patch_data = {
        'title': 'bye',
        'account_id': 1,
        'category': 1,
        'goal': 'say-good-bye',
        'start_time': '11:00:00',
        'days': ['MON', 'WED', 'THU']
    }
    # when
    client.patch(
        f'{routines_router_url}/{routine.id}',
        json=patch_data
    )
    # then
    days = db.query(RoutineDay.day).filter(RoutineDay.routine_id == routine.id).all()
    result = []
    for day in days:
        result.append(day[0].value)
    result.sort()
    assert_that(result).is_equal_to(sorted(patch_data['days']))


def test_루틴_값_수정하는데_요일이_아닌_다른_것(db: Session, client: TestClient):
    # given
    data = {
        'title': 'yes',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'start_time': '10:00:00',
        'days': ['FRI', 'SAT', 'SUN']
    }
    client.post(
        f'{routines_router_url}',
        json=data
    )
    routine: Routine = db.query(Routine).filter(and_(Routine.title == data['title'], Routine.account_id == data['account_id'])).first()
    patch_data = {
        'title': 'bye',
        'account_id': 1,
        'category': 1,
        'goal': 'say-good-bye',
        'start_time': '11:00:00',
        'days': ['FRI', 'SAT', 'SUN']
    }
    # when
    client.patch(
        f'{routines_router_url}/{routine.id}',
        json=patch_data
    )
    # then
    routine: Routine = db.query(Routine).filter(and_(Routine.title == patch_data['title'], Routine.account_id == patch_data['account_id'])).first()
    assert_that(routine.title).is_equal_to(patch_data['title'])
    assert_that(routine.goal).is_equal_to(patch_data['goal'])
    assert_that(str(routine.start_time)).is_equal_to(patch_data['start_time'])


@complex_transaction
def test_루틴_수행여부_값_저장_오늘이_수행하는_날일_때(db: Session, client: TestClient):
    # given
    now = get_now()
    weekday = now.weekday()
    weekday = Week.get_weekday(weekday)
    create = {
        'title': 'wake_up',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=create
    )
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)
    routine_data = {
        'result': 'DONE',
        'weekday': weekday.value,
        'date': date.strftime("%Y-%m-%d")
    }
    # when
    response = client.post(
        f'{routines_router_url}/{routine.id}/check-result',
        json=routine_data
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


@complex_transaction
def test_루틴_결과_체크하는데_Default인_경우(db: Session, client: TestClient):
    # given
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    now = get_now()
    weekday = now.weekday()
    weekday = Week.get_weekday(weekday)
    days.remove(weekday)
    create = {
        'title': 'wake_up',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': days
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=create
    )
    routine = db.query(Routine).first()
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)
    routine_data = {
        'result': 'DONE',
        'weekday': weekday.value,
        'date': date.strftime("%Y-%m-%d")
    }
    # when
    response = client.post(
        f'{routines_router_url}/{routine.id}/check-result',
        json=routine_data
    )
    # then
    assert_that(response.status_code).is_equal_to(200)
    routine_result = db.query(RoutineResult).filter(and_(RoutineResult.routine_id == routine.id, RoutineResult.yymmdd == date)).first()
    assert_that(routine_result).is_not_none()
    assert_that(routine_result.result).is_equal_to(Result.DONE)
    routine_results = db.query(RoutineResult).all()
    assert_that(len(routine_results)).is_equal_to(1)


@complex_transaction
def test_루틴_디테일_조회(db: Session, client: TestClient):
    # given
    data = {
        'title': 'time_test',
        'account_id': 1,
        'category': 1,
        'goal': 'daily',
        'is_alarm': True,
        'start_time': '10:00:00',
        'days': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    }
    # when
    response = client.post(
        f'{routines_router_url}',
        json=data
    )
    assert_that(response.status_code).is_equal_to(200)
    routine: Routine = db.query(Routine).filter(Routine.title == data['title']).first()
    response = client.get(
        f'{routines_router_url}/{routine.id}'
    )
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to(HttpStatus.ROUTINE_DETAIL_OK.value)
    assert_that(message['msg']).is_equal_to(ROUTINE_GET_MESSAGE)
    assert_that(body['id']).is_equal_to(routine.id)
    assert_that(body['title']).is_equal_to(data['title'])
    assert_that(body['category']).is_equal_to(data['category'])
    assert_that(body['goal']).is_equal_to(data['goal'])
    assert_that(len(body['days'])).is_equal_to(7)


def test_루틴_수행여부_취소(db: Session, client: TestClient):
    # given
    """
    수행요일 확인
    루틴 아이디, 해당 날짜
    :return:
    """
    # when
    """
    루틴 결과를 실패 관련 값으로 변경
    """
    # then
    """
    성공 여부 전달
    {
        'message' : {
            'status' : 'ROUTINE_RESULT_CANCEL_OK',
            'msg': '루틴 결과 취소에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_루틴_삭제(db: Session, client: TestClient):
    # given
    """
    :parameter: 루틴 아이디, 유저 아이디
    :return:
    """
    # when
    """
    회고를 살리느냐 안살리느냐에 따라 다를 것 같은데
    우선 살리는 방향으로 진행할 예정
    루틴에 관한 정보만 삭제 진행
    """
    # then
    """
    성공 여부 전달
    {
        'message' : {
            'status' : 'ROUTINE_DELETE',
            'msg': '루틴 삭제에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }    
    """


def test_루틴_순서_변경(db: Session, client: TestClient):
    # given
    """
    @:param: list(루틴아이디, 순서), 유저 아이디
    :return:
    """
    # when
    """
    for문 돌려서 dirty checking을 통해 순서 값 변경
    """
    # then
    """
    성공여부 전달
    {
        'message' : {
            'status' : 'ROUTINE_CHANGE_OK',
            'msg': '루틴 순서 변경에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """
