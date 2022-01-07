from assertpy import assert_that

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_루틴_생성_테스트():
    request = {
        'title': 'hello',
        'account_id': 1,
        'category': 0,
        'goal': 'world',
        'start_time': '10:30:00',
        'days': ['MON', 'WED', 'FRI']
    }
    response = client.request('post', '/api/v1/routine/create', json=request)
    assert_that(response.status_code).is_not_equal_to('200')
    result = response.json()
    assert_that(result).is_not_none()
    data = result['data']
    assert_that(data['success']).is_true()
    assert_that(result['message']).is_equal_to({'status': 'ROUTINE_OK', 'msg': '루틴 생성에 성공하셨습니다.'})


def test_루틴_생성_성공했을_때():
    # given
    """
    @:parameter: 루틴 이름, 루틴 목표, 카테고리, 루틴 요일, 루틴 시간 여부, 알람 여부, 유저 아이디,
    :return:
    """
    # when
    """
    repository 통해 생성
    """
    # then
    """
    단순히 성공 여부만 전달
    {
        'message' : {
            'status' : 'ROUTINE_CREATE_OK',
            'msg': '루틴 생성에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """

def test_루틴_생성_루틴_이름_공백일_때():
    # given
    """
    루틴 이름 또는 루틴 목표가 공백일 때
    :return:
    """
    # when
    """
    사전 validation에서 필터링
    """
    # then
    """
    실패 값 전달
     {
        'message' : {
            'status' : 'ROUTINE_CREATE_BAD_REQUEST',
            'msg': '루틴 생성에 실패하셨습니다.'
        },
        'data': {
            'detail': JSON
        }
    }   
    """

def test_루틴_생성_카테고리_선택하지_않을_때():
    # given
    """
    카테고리 값이 null로 들어올 때
    :return:
    """
    # when
    """
    default로 etc로 지정
    """
    # then
    """
    성공 값 전달
     {
        'message' : {
            'status' : 'ROUTINE_CREATE_BAD_REQUEST',
            'msg': '루틴 생성에 실패하셨습니다.'
        },
        'data': {
            'detail': JSON
        }
    }
    """

def test_루틴_생성_요일_값_전달받지_못할_때():
    # given
    """
    루틴 값을 받지 못했을 때
    :return:
    """
    # when
    """
    validation으로 '루틴 요일을 선택해주세요' 와 비슷한 문구와 함께 에러 발생
    """
    # then
    """
    실패 값 전달
     {
        'message' : {
            'status' : 'ROUTINE_CREATE_BAD_REQUEST',
            'msg': '루틴 생성에 실패하셨습니다.'
        },
        'data': {
            'detail': JSON
        }
    }    
    """

def test_루틴_생성_알람보내기값이_null일_때():
    # given
    """
    알람 보내기 값이 null 일 때
    :return:
    """
    # when
    """
    default 로 false 값으로 생성
    """
    # then
    """
    성공 값 전달
    {
        'message' : {
            'status' : 'ROUTINE_CREATE_OK',
            'msg': '루틴 생성에 성공하셨습니다.'
        },
        'data': {
            'success': true
        }
    }
    """

def test_루틴_값_수정하는데_요일일_때():
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

def test_루틴_값_수정하는데_요일이_아닌_다른_것():
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

def test_루틴_수행여부_값_저장():
    # given
    """
    루틴 수행 여부 값, 루틴 아이디, 해당 날짜
    신규 테이블 필요할 듯
    루틴 수행 여부 저장하는 테이블

    TABLE
    고유 아이디 | 루틴 아이디 | 루틴 데이 아이디 | 루틴 수행 여부 | 해당 날짜 |체크한 시간

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

def test_루틴_수행여부_취소():
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

def test_루틴_삭제():
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

def test_루틴_전체_조회():
    # given
    """
    @:param: 유저 아이디
    :return:
    """
    # when
    """
    루틴 전체 조회
    repository 조회
    """
    # then
    """
        [
        {
            "routine_id" : 1,
            "title" : "아침에 신문 읽기",
            "aim": "시사경영 3개씩 매일 읽기",
            "start_time": "07:00",
            "routine_result": {
                result: "DONE"
            }
        },
        {
            "routine_id" : 2,
            "title" : "아침에 시리얼 먹기",
            "aim": "냠냠",
            "start_time": "06:00",
            "routine_result": {
                result: "YET"
            }
        },
    ]
    """
    
def test_루틴_순서_변경():
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

