import freezegun
from assertpy import assert_that
from fastapi import UploadFile
from sqlalchemy.orm import Session

from base.exception.exception import MinningException
from base.utils.constants import HttpStatus
from main import app
from fastapi.testclient import TestClient

from retrospect.models.retrospect import Retrospect
from retrospect.models.snapshot import Snapshot
from retrospect.service.retrospect_service import put_detail_retrospect, delete_detail_retrospect
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.service.routine_service import create_routine
from routine.schemas import RoutineCreateRequest
from test.conftest import maintain_idempotent
from retrospect.constants.retrospect_message import RETROSPECT_CREATE_MESSAGE, RETROSPECT_ALREADY_EXISTS, RETROSPECT_UPDATE_MESSAGE, RETROSPECT_DELETE_MESSAGE, RETROSPECT_NOT_FOUND_ID

client = TestClient(app)
retrospect_router_url = '/api/v1/retrospects'


@maintain_idempotent
def test_회고_정상적으로_생성(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-01-31'):
        routine_data = RoutineCreateRequest(
            title='time_test', category='SELF',
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
        filepath = './resource/test.png'
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
            title='time_test', category='SELF',
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
        filepath = './resource/test.png'
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
            title='time_test', category='SELF',
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
            title='time_test', category='SELF',
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
            title='first', category='SELF',
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
        filepath = './resource/test2.png'
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
            title='first', category='SELF',
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
        filepath = './resource/test.png'
        with open(filepath, 'rb') as f:
            put_detail_retrospect(retrospect_id=retrospect.id, content='수정했어요', db=db, image=UploadFile(filename='test.png', file=f), account=1)
            change_retrospect = db.query(Retrospect).filter(Retrospect.id == retrospect.id).first()
            assert_that(change_retrospect.content).is_equal_to('수정했어요')


@maintain_idempotent
def test_회고_삭제할_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-03'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.THU]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-03'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )
        # when
        retrospect = db.query(Retrospect).first()
        response = client.delete(
            f'{retrospect_router_url}/{retrospect.id}',
            headers={'account': '1'}
        )
        # then
        message = response.json()['message']
        assert_that(response.status_code).is_equal_to(200)
        assert_that(message['status']).is_equal_to(HttpStatus.RETROSPECT_DELETE_OK.value)
        assert_that(message['msg']).is_equal_to(RETROSPECT_DELETE_MESSAGE)


@maintain_idempotent
def test_디테일_회고_조회(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-03'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.THU]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-03'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )
        # when
        retrospect = db.query(Retrospect).first()
        response = client.get(
            f'{retrospect_router_url}/{retrospect.id}',
            headers={'account': '1'}
        )
        body = response.json()['data']
        assert_that(body['id']).is_equal_to(retrospect.id)
        assert_that(body['title']).is_equal_to(retrospect.title)
        assert_that(body['content']).is_equal_to(retrospect.content)


@maintain_idempotent
def test_가져오는데_유저아이디가_틀릴_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-04'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.FRI]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-04'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )
        # when
        retrospect = db.query(Retrospect).first()
        response = client.get(
            f'{retrospect_router_url}/{retrospect.id}',
            headers={'account': '2'}
        )
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()['body']).is_equal_to(RETROSPECT_NOT_FOUND_ID)


@maintain_idempotent
def test_회고_수정하는데_유저아이디가_틀릴_때(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-04'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.FRI]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-04'
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
        filepath = './resource/test2.png'
        # when
        with open(filepath, 'rb') as f:
            response = client.put(
                f'{retrospect_router_url}/{retrospect.id}',
                data=put_data,
                files={'image': ('test2', f, 'png')},
                headers={'account': '2'}
            )
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()['body']).is_equal_to(RETROSPECT_NOT_FOUND_ID)


@maintain_idempotent
def test_회고_삭제할_때_유저아이디_불일치(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-04'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.FRI]
        )
        create_routine(db=db, routine=routine_data, account=1)
        routine = db.query(Routine).first()
        data = {
            'routine_id': routine.id,
            'content': '그렇게 되었습니다.',
            'date': '2022-02-04'
        }
        client.post(
            f'{retrospect_router_url}',
            data=data,
            headers={'account': '1'}
        )

        retrospect = db.query(Retrospect).first()
        assert_that(delete_detail_retrospect).raises(MinningException).when_called_with(retrospect_id=retrospect.id, db=db, account=2)


@maintain_idempotent
def test_당일_작성한_회고_리스트_조회(db: Session, client: TestClient):
    # given
    with freezegun.freeze_time('2022-02-05'):
        routine_data = RoutineCreateRequest(
            title='first', category='SELF',
            goal='one', is_alarm=True,
            start_time='10:00:00',
            days=[Week.SAT]
        )
        create_routine(db=db, routine=routine_data, account=1)

        routine_data = RoutineCreateRequest(
            title='second', category='SELF',
            goal='two', is_alarm=True,
            start_time='10:00:00',
            days=[Week.SAT]
        )
        create_routine(db=db, routine=routine_data, account=1)

        routines = db.query(Routine).all()
        for routine in routines:
            data = {
                'routine_id': routine.id,
                'content': '그렇게 되었습니다.',
                'date': '2022-02-05'
            }
            client.post(
                f'{retrospect_router_url}',
                data=data,
                headers={'account': '1'}
            )

        response = client.get(
            f'{retrospect_router_url}?date=2022-02-05',
            headers={'account': '1'}
        )
        assert_that(response.status_code).is_equal_to(200)
        result = response.json()
        data = result['data']
        assert_that(len(data)).is_equal_to(2)
        first_data = data[0]
        assert_that(first_data).contains_key('id', 'title', 'content', 'url')
