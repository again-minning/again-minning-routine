import freezegun
from assertpy import assert_that
from fastapi import UploadFile
from sqlalchemy.orm import Session

from base.utils.constants import HttpStatus
from main import app
from fastapi.testclient import TestClient

from retrospect.models.retrospect import Retrospect
from retrospect.models.snapshot import Snapshot
from retrospect.repository.retrospect_repository import put_detail_retrospect
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
def test_회고_중복_체크(db: Session, client: TestClient):
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
            'content': '그렇게 되었습니다.',
            'date': '2022-01-31'
        }
        filepath = '../resource'
        # when
        with open(filepath, 'rb') as f:
            client.post(
                f'{retrospect_router_url}',
                data=data,
                files={'image': ('test', f, 'png')},
                headers={'account': '1'}
            )
        duplicate_data = {
            'routine_id': routine.id,
            'content': '그렇게는 안될겁니다',
            'date': '2022-01-31'
        }
        # when
        response = client.post(
            f'{retrospect_router_url}',
            data=duplicate_data,
            headers={'account': '1'}
        )
        result = response.json()
        assert_that(response.status_code).is_equal_to(400)
        assert_that(result['body']).is_equal_to(RETROSPECT_ALREADY_EXISTS)


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


@maintain_idempotent
def test_회고_수정할_때_이미지에_대해서(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-01'):
        routine_data = RoutineCreateRequest(
            title='first', category=1,
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.TUE]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-01'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )

        retrospect = db.query(Retrospect).first()
        put_data = {
            'content': '그렇게 되었습니다.'
        }
        filepath = '../resource'
        # when
        with open(filepath, 'rb') as f:
            response = client.put(
                f'{retrospect_router_url}/{retrospect.id}',
                data=put_data,
                files={'image': ('test2', f, 'png')},
                headers={'account': '1'}
            )
        # then
        result = response.json()
        message = result['message']
        assert_that(message['status']).is_equal_to(HttpStatus.RETROSPECT_UPDATE_OK.value)
        assert_that(message['msg']).is_equal_to(RETROSPECT_UPDATE_MESSAGE)
        snapshot = db.query(Snapshot).filter(Snapshot.retrospect_id == retrospect.id).first()
        assert_that(snapshot.url).is_equal_to('test2')


@maintain_idempotent
def test_회고_수정할_때_글_내용_수정할_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-01'):
        routine_data = RoutineCreateRequest(
            title='first', category=1,
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.TUE]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-01'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )

        retrospect = db.query(Retrospect).first()
        filepath = '../resource'
        with open(filepath, 'rb') as f:
            put_detail_retrospect(retrospect_id=retrospect.id, content='수정했어요', db=db, image=UploadFile(filename='test.png', file=f))
            change_retrospect = db.query(Retrospect).filter(Retrospect.id == retrospect.id).first()
            assert_that(change_retrospect.content).is_equal_to('수정했어요')


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
