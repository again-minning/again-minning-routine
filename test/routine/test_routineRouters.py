import datetime

from assertpy import assert_that
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.utils.time import get_now
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from test.conftest import client, complex_transaction

client = client


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
        '/api/v1/routine',
        json=data
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to('루틴 생성에 성공하셨습니다.')
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
        '/api/v1/routine',
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
        '/api/v1/routine',
        json=data
    )
    assert_that(response.status_code).is_equal_to(200)
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    routine_id = routine.id
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    assert_that(routine_results[0].result).is_equal_to('DEFAULT')


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
        '/api/v1/routine',
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
    assert_that(path).is_equal_to('/api/v1/routine')
    assert_that(msg).is_equal_to('제목 문구를 적어주세요.')
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
        '/api/v1/routine',
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
    assert_that(path).is_equal_to('/api/v1/routine')
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
        '/api/v1/routine',
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
    assert_that(path).is_equal_to('/api/v1/routine')
    assert_that(msg).is_equal_to('최소 한 개의 요일을 선택해주세요')
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
        '/api/v1/routine',
        json=data
    )
    # then
    result = response.json()
    message = result['message']
    body = result['data']
    assert_that(message['status']).is_equal_to('ROUTINE_CREATE_OK')
    assert_that(message['msg']).is_equal_to('루틴 생성에 성공하셨습니다.')
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
        '/api/v1/routine',
        json=data
    )
    account_id = 1
    today = get_now()
    # when
    response = client.get(
        f'/api/v1/routine/{account_id}?today={today.strftime("%Y-%m-%d")}',
    )
    result = response.json()
    message = result['message']
    body = result['data'][0]
    # then
    assert_that(message['status']).is_equal_to('ROUTINE_LIST_OK')
    assert_that(message['msg']).is_equal_to('루틴 조회에 성공하셨습니다.')
    assert_that(body['title']).is_equal_to(data['title'])
    assert_that(body['goal']).is_equal_to(data['goal'])
    assert_that(body['start_time']).is_equal_to(data['start_time'])
    assert_that(body['result']).is_equal_to('NOT')


def test_루틴_조회_이때_루틴결과값이_여러개이지만_하나만_가져오는지(db: Session, client: TestClient):
    # TODO
    """
    현재 잘 안됨
    다음 이슈에서 진행해야 할 것 같다. 너무 길어짐 ...
    """
    pass

def test_루틴_값_수정하는데_요일일_때(db: Session, client: TestClient):
    # given
    """
    기존 루틴 값 그대로, 루틴 요일 변경
    :return:
    """
    # when
    """
    set 자료형을 이용해 차집합 사용
    기존 - 새로운 : 삭제할 대상
    새로운 - 기존: 추가될 대상
    기존 and 새로운 : 보존할 대상
    보존할 대상만 있는 경우 pass
    그렇지 않을 경우 수정 작업
    """
    # then
    """
    merge => 그 이유는 기존 값도 클라에서 제공할 예정이라서
    {
        'message' : {
            'status' : 'ROUTINE_UPDATE_OK',
            'msg': '루틴 수정에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_루틴_값_수정하는데_요일이_아닌_다른_것(db: Session, client: TestClient):
    # given
    """
    루틴 생성 값 그대로 받아 들임
    :return:
    """
    # when
    """
    그대로 merge 진행
    """
    # then
    """
    성공 여부 전달
    {
        'message' : {
            'status' : 'ROUTINE_UPDATE_OK',
            'msg': '루틴 수정에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_루틴_수행여부_값_저장(db: Session, client: TestClient):
    # given
    """
    루틴 수행 여부 값, 루틴 아이디, 해당 날짜
    신규 테이블 필요할 듯
    루틴 수행 여부 저장하는 테이블

    TABLE
    고유 아이디 | 루틴 아이디 | 해당 수행 요일 | 루틴 수행 여부 | 해당 날짜

    :return:
    """
    # when
    """
    수행 요일인지 확인
    루틴 수행 여부 저장
    왜 회고를 통해 확인을 안한 이유?
    회고를 통해서 완료 여부를 확인을 하지 않고 온전히 루틴을 수행 했는지 안했는지에 대한 값을 저장하는 게 고객의 요구 사항을 처리하는 게 더 용이하다고 판단
    고객의 요구에 따라 그냥 내가 루틴을 수행 했는지 안 했는지 체크하는 용도로만 사용할 수 있을 것 같음
    만일 회고의 값을 비교한다고 해도 어려울 것이 없음 그냥 회고의 값을 비교하는 것만 로직에 추가하면 되니까
    """
    # then
    """
    성공 여부
    {
        'message' : {
            'status' : 'ROUTINE_RESULT_CREATE_OK',
            'msg': '루틴 결과 생성에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }    
    """


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
