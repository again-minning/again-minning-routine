from assertpy import assert_that

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_주_리포트_생성():
    # given
    """
    celery 작업큐를 통해 생성
    필요한 것은 Routine, RoutineResult,RoutineDay
    :return:
    """
    # when
    """
    루틴과 루틴데이 그리고 루틴결과를 조인을 한다.
    조인을 한 다음 각 루틴 별 진행한 요일과 결과를 가져온다.
    그 결과 값에 대한 리스트를 만든다.
    완료, 부분완료, 미완료에 대한 갯수를 카운팅한다.
    3개의 갯수로 달성률을 계산해준다.
    그 결과값을 리포트 필드에 넣어준다.
    ---
    리포트와 같은 데이터들은 수정되지 않고 저장되는 결과값
    기본적으로 조인이 많이 필요로 하는 테이블
    noSQL 데이터베이스가 적합하다고 판단 -> mongodb(document db)
    그래서 리포트 결과값들을 document db에 저장할려고 함
    ---
    report_id
    account_id
    created_at -> yyyy-mm-dd
    달성률
    완료
    부분완료
    미완료
    루틴 결과 List -> [ 루틴 아이디, 루틴 타이틀, 카테고리, 루틴 결과 (해당 요일, 결과) ]
    ---
    몽고디비에서 논리적으로는 분리되어도 물리적으로 통으로 저장이 된다.
    """
    # then
    """
    저장된 값을 그대로 뿌려준다.
    """


def 월_리포트_생성():
    # given
    """
    celery 작업큐를 통해 진행
    report created_at 을 yyyy-mm-01 <= created_at <=yyyy-mm-31
    :return:
    """
    # when
    """
    월 리포트
    current month - 1 을 했을 때의 날짜를 필터링해서 주 리포트를 다 가져온다.
    주 리포트의 주차 별 정보를 저장한다. [ 몽고 디비 Arrays 필드 사용)
    카테고리 별로 저장하는 로직을 작성하는데 이 때 해야 할 작업은
    - 카테고리 별 갯수
    - 카테고리 안에 루틴 별 상세 정보
        - 타이틀, 완료, 부분완료, 미완료
    
    """
    # then
    """
    {
        "주차별달성률" : [ 80, 42, 100, 90],
        "카테고리별 비중":{
            0 : 33,
            1: 20,
            2: 7,
            3: 15,
            4: 25
        }
        "카테고리별 상세내용": {
            0: [
                routine_id : {
                    '제목' : '확언하기',
                    '완료' : 90,
                    '부분완료': 10,
                    '미완료' : 0
                },
                routine_id : {
                    '제목' : '확언하기',
                    '완료' : 90,
                    '부분완료': 10,
                    '미완료' : 0
                }
            ],
            1: [
                routine_id : {
                    '제목' : '확언하기',
                    '완료' : 90,
                    '부분완료': 10,
                    '미완료' : 0
                },
                routine_id : {
                    '제목' : '확언하기',
                    '완료' : 90,
                    '부분완료': 10,
                    '미완료' : 0
                }
            ],
            ... 
        }
    }
    """