from assertpy import assert_that

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_회고_정상적으로_생성():
    # given
    """
    @:param: 사진, 루틴 아이디, 내용, 유저 아이디
    루틴 사전 생성
    :return:
    """
    # when
    """
    repository 불러서 해당 값을 넣는다. 
    """
    # then
    """
    조회를 통해 해당 값이 잘 들어가 있는 지 확인
    {
        'message' : {
            'status' : 'RETROSPECT_CREATE_OK',
            'msg': '회고 생성에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """


def test_회고_생성_성공_이미지_파라미터가_없을_때():
    # given
    """
    @:parameter: 사진(x), 루틴 아이디, 내용, 유저 아이디
    루틴 사전 생성
    :return:
    """
    # when
    """
    repository 불러서 해당 값을 넣는다.(이미지가 없음)
    """
    # then
    """
    이미지 없어도 생성 완료
        {
        'message' : {
            'status' : 'RETROSPECT_CREATE_OK',
            'msg': '회고 생성에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """

def test_회고_생성_실패_루틴_정보가_없을_때():
    # given
    """
    @:parameter: 사진, 내용, 루틴 아이디 x, 유저 아이디
    :return:
    """
    # when
    """
    생성 시도
    """
    # then
    """
    에러 확인
        {
        'message' : {
            'status' : 'RETROSPECT_BAD_REQUEST',
            'msg': '회고 생성에 실패하셨습니다..'
        },
        'data': {
            'detail': JSON
        }
    }
    """

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
