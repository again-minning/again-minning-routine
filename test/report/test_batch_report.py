import json
import random

from assertpy import assert_that
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from test.report.utils import __make_report_data

from routine.constants.category import Category
from test.conftest import maintain_idempotent_async

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
