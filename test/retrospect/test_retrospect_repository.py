import freezegun
from assertpy import assert_that
from sqlalchemy.orm import Session

from base.utils.constants import HttpStatus
from main import app
from fastapi.testclient import TestClient

from routine.constants.week import Week
from routine.models.routine import Routine
from routine.repository.routine_repository import create_routine
from routine.schemas import RoutineCreateRequest
from test.conftest import maintain_idempotent
from retrospect.constants.retrospect_message import *
client = TestClient(app)
retrospect_router_url = '/api/v1/retrospects'


@maintain_idempotent
def test_회고_정상적으로_생성(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-31'):
        routine_data = RoutineCreateRequest(
            title='time_test', category=1,
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.MON]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'title': '회고생성',
            'content': '그렇게 되었습니다.',
            'date': '2022-01-31'
        }
        filepath = '../resource'
        # when
        with open(filepath, 'rb') as f:
            response = client.post(
                f'{retrospect_router_url}',
                data=data,
                files={'image': ('test', f, 'png')},
                headers={'account': '1'}
            )
        # then
        result = response.json()
        message = result['message']
        assert_that(message['status']).is_equal_to(HttpStatus.RETROSPECT_CREATE_OK.value)
        assert_that(message['msg']).is_equal_to(RETROSPECT_CREATE_MESSAGE)


@maintain_idempotent
def test_회고_생성_성공_이미지_파라미터가_없을_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-31'):
        routine_data = RoutineCreateRequest(
            title='time_test', category=1,
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.MON]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'title': '회고생성',
            'content': '그렇게 되었습니다.',
            'date': '2022-01-31'
        }
        # when
        response = client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )
        # then
        result = response.json()
        message = result['message']
        assert_that(message['status']).is_equal_to(HttpStatus.RETROSPECT_CREATE_OK.value)
        assert_that(message['msg']).is_equal_to(RETROSPECT_CREATE_MESSAGE)


@maintain_idempotent
def test_회고_생성_실패_루틴_정보가_없을_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-31'):
        routine_data = RoutineCreateRequest(
            title='time_test', category=1,
            goal='daily', is_alarm=True,
            start_time='10:00:00',
            days=[Week.MON]
        )
        create_routine(db=db, routine=routine_data, account=1)
        data = {
            'title': '회고생성',
            'content': '그렇게 되었습니다.',
            'date': '2022-01-31'
        }
        # when
        response = client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )
        # then
        assert_that(response.status_code).is_equal_to(400)


def test_회고_수정할_때_이미지에_대해서():
    # given
    """
    @:parameter: 이미지, 회고 아이디, 유저 아이디
    :return:
    """
    # when
    """
    생성일과 현재 시간을 비교해 3일이 지났는 지 확인
    (토요일에 작성했으면 월요일까지 수정이 가능) 
    기존 이미지 삭제 및 새 이미지 아이디와 회고 아이디 연결
    성공 여부 전달
    """
    # then
    """
    성공 여부 전달
        {
        'message' : {
            'status' : 'RETROSPECT_UPDATE_OK',
            'msg': '회고 수정에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_회고_수정할_때_글_내용_수정할_때():
    # given
    """
    @:parameter: 회고 아이디, 글 내용, 유저 아이디
    :return:
    """
    # when
    """
    생성일과 현재 시간을 비교해 3일이 지났는 지 확인
    (토요일에 작성했으면 월요일까지 수정이 가능) 
    기존 콘텐츠 날리고 새 콘텐츠로 변경
    """
    # then
    """
    성공 여부 전달
            {
        'message' : {
            'status' : 'RETROSPECT_UPDATE_OK',
            'msg': '회고 수정에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_회고_삭제할_때():
    # given
    """
    @:parameter: 회고 아이디, 유저 아이디
    :return:
    """
    # when
    """
    삭제 진행
    삭제 진행할 때 회고 내용만 삭제되고 이에 대한 수행 여부는 존재해야 한다.
    """
    # then
    """
    성공 여부 전달
            {
        'message' : {
            'status' : 'RETROSPECT_DELETE_OK',
            'msg': '회고 삭제에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_당일_해야하는_회고_리스트_조회():
    # given
    """
    @:param: account_id, 요일
    :return:
    """
    # when
    """
    당일 요일에 해당하는 루틴 목록 조회 where 오늘 회고 했는 지 안했는 지 조회
    조회 로직은 회고와 left outer join을 해서 retrospect이 null인 것을 허용하면서 조회를 한다.
    처음 조회를 할 때 쌩으로 다 조회하지 말고 조회 할 때 필요한 값만 조회를 한다. 
    """
    # then
    """
    {
        'message' : {
            'status' : 'RETROSPECT_SELECT_OK',
            'msg': '회고 조회에 성공하셨습니다.'
        },
        'data': {
            [
                {
                    'retrospect_id' : int or null,
                    'routine_id': int
                    'title' : str,
                    'content': str,
                    'sequence': int
                },
                {
                    'retrospect_id' : int or null,
                    'routine_id': int
                    'title' : str,
                    'content': str,
                    'sequence': int
                },
            ]
        }
    }
    """
