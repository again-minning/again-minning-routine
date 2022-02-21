import json
import random
from datetime import timedelta
from test.conftest import maintain_idempotent_async
from assertpy import assert_that
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from base.utils.time import convert_str2datetime
from routine.constants.category import Category

routines_router_url = '/api/v1/routines'
routines_batch_router_url = '/api/v1/batch-routines'
report_batch_router_url = '/api/v1/batch-reports'


@maintain_idempotent_async()
async def test_주_리포트_생성(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    # given
    data = await __make_report_data()
    response = await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )
    data = response.json()
    assert_that(data['done_count']).is_equal_to(5)
    assert_that(data['not_count']).is_equal_to(3)
    assert_that(data['try_count']).is_equal_to(0)
    assert_that(data['achievement_rate']).is_equal_to(0.625)
    assert_that(len(data['routine_results'])).is_equal_to(8)


@maintain_idempotent_async()
async def test_월_리포트_생성(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    categories = [Category.DAILY.value, Category.SELF.value, Category.HEALTH.value, Category.MIRACLE.value]
    categories = random.sample(categories, 3)
    data = await __make_report_data(date='2022-01-10', categories=categories)
    await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )

    data = await __make_report_data(date='2022-01-17', categories=categories)
    await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )

    data = await __make_report_data(date='2022-01-24', categories=categories)
    await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )

    data = await __make_report_data(date='2022-01-31', categories=categories)
    await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )

    response = await async_client.post(
        f'{report_batch_router_url}/month?account-id=1'
    )
    data = response.json()
    category_detail = data['category_detail']
    total = 0
    for k, v in category_detail.items():
        total += len(v.keys())
    assert_that(total).is_equal_to(8)
    total = 0
    category_routine_count = data['category_routine_count']
    for k, v in category_routine_count.items():
        total += v
    assert_that(total).is_equal_to(8)
    assert_that(data['weekly_achievement_rate'][0]).is_equal_to(0.625)


async def __make_report_data(date="2022-02-07 00:00:00", categories=('SELF', 'MIRACLE', 'DAILY')):
    data = {
        "routines": [
            {
                "title": "글5",
                "category": categories[0],
                "id": 6,
                "account_id": 1
            }, {
                "title": "글6",
                "category": categories[0],
                "id": 7,
                "account_id": 1
            }, {
                "title": "글7",
                "category": categories[1],
                "id": 8,
                "account_id": 1
            }, {
                "title": "글8",
                "category": categories[1],
                "id": 9,
                "account_id": 1
            }, {
                "title": "글9",
                "category": categories[2],
                "id": 10,
                "account_id": 1
            }, {
                "title": "글10",
                "category": categories[2],
                "id": 11,
                "account_id": 1
            }, {
                "title": "글11",
                "category": categories[0],
                "id": 12,
                "account_id": 1
            }, {
                "title": "글12",
                "category": categories[0],
                "id": 13,
                "account_id": 1
            }

        ],
        "routine_results": [
            {
                "routine_id": 6,
                "date": date,
                "result": "DONE"
            }, {
                "routine_id": 7,
                "date": date,
                "result": "DONE"
            }, {
                "routine_id": 8,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 9,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 10,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 11,
                "date": str(convert_str2datetime(date) + timedelta(days=2)),
                "result": "DONE"
            }, {
                "routine_id": 12,
                "date": str(convert_str2datetime(date) + timedelta(days=2)),
                "result": "DONE"
            }, {
                "routine_id": 13,
                "date": str(convert_str2datetime(date) + timedelta(days=5)),
                "result": "DONE"
            }
        ]
    }
    return data
