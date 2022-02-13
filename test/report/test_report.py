import json

import pytest
from assertpy import assert_that
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

routines_router_url = '/api/v1/routines'
routines_batch_router_url = '/api/v1/batch-routines'
report_batch_router_url = '/api/v1/batch-reports'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_주_리포트_생성(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    # given
    data = {
        "routines": [
                {
                    "title": "글5",
                    "category": 1,
                    "id": 6,
                    "account_id": 1
                }, {
                    "title": "글6",
                    "category": 1,
                    "id": 7,
                    "account_id": 1
                }, {
                    "title": "글7",
                    "category": 1,
                    "id": 8,
                    "account_id": 1
                }, {
                    "title": "글8",
                    "category": 1,
                    "id": 9,
                    "account_id": 1
                }, {
                    "title": "글9",
                    "category": 1,
                    "id": 10,
                    "account_id": 1
                }, {
                    "title": "글10",
                    "category": 1,
                    "id": 11,
                    "account_id": 1
                }, {
                    "title": "글11",
                    "category": 1,
                    "id": 12,
                    "account_id": 1
                }, {
                    "title": "글12",
                    "category": 1,
                    "id": 13,
                    "account_id": 1
                }

            ],
        "routine_results": [
            {
                "routine_id": 6,
                "date": "2022-02-07 00:00:00",
                "result": "DONE"
            }, {
                "routine_id": 7,
                "date": "2022-02-07 00:00:00",
                "result": "DONE"
            }, {
                "routine_id": 8,
                "date": "2022-02-07 00:00:00",
                "result": "NOT"
            }, {
                "routine_id": 9,
                "date": "2022-02-07 00:00:00",
                "result": "NOT"
            }, {
                "routine_id": 10,
                "date": "2022-02-07 00:00:00",
                "result": "NOT"
            }, {
                "routine_id": 11,
                "date": "2022-02-09 00:00:00",
                "result": "DONE"
            }, {
                "routine_id": 12,
                "date": "2022-02-09 00:00:00",
                "result": "DONE"
            }, {
                "routine_id": 13,
                "date": "2022-02-12 00:00:00",
                "result": "DONE"
            }
        ]
    }
    response = await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )
    data = response.json()
    assert_that(data['done_count']).is_equal_to(5)
    assert_that(data['none_count']).is_equal_to(3)
    assert_that(data['try_count']).is_equal_to(0)
    assert_that(data['achievement_rate']).is_equal_to(0.625)
    assert_that(len(data['routine_results'])).is_equal_to(8)


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
        }
    }
    """
