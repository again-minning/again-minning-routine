import json
import random

import freezegun
from assertpy import assert_that
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from base.utils.constants import HttpStatus
from base.utils.time import get_now, get_start_datetime
from report.constants.report_message import REPORT_NOT_FOUND
from routine.constants.category import Category
from test.conftest import maintain_idempotent_async
from test.report.utils import __make_report_data

report_router_url = '/api/v1/reports'
routines_batch_router_url = '/api/v1/batch-routines'
report_batch_router_url = '/api/v1/batch-reports'


@maintain_idempotent_async()
@freezegun.freeze_time('2022-02-14')
async def test_주_리포트_조회(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    # given
    data = await __make_report_data()
    await async_client.post(
        f'{report_batch_router_url}/week',
        content=json.dumps(data)
    )
    today = get_start_datetime(get_now()).strftime('%Y-%m-%dT%H:%M:%S')
    # when
    response = await async_client.get(
        f'{report_router_url}/week?date={today}',
        headers={'account': '1'}
    )
    # then
    result = response.json()
    message = result['message']
    data = result['data']
    assert_that(response.status_code).is_equal_to(200)
    assert_that(message['status']).is_equal_to(HttpStatus.REPORT_DETAIL_OK.value)
    assert_that(data['done_count']).is_equal_to(5)
    assert_that(data['not_count']).is_equal_to(3)
    assert_that(len(data['routine_results'])).is_equal_to(8)


@maintain_idempotent_async()
async def test_주_리포트_없을_때_조회(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    # given
    with freezegun.freeze_time('2022-02-14'):
        data = await __make_report_data()
        response = await async_client.post(
            f'{report_batch_router_url}/week',
            content=json.dumps(data)
        )
    with freezegun.freeze_time('2022-02-21'):
        today = get_start_datetime(get_now()).strftime('%Y-%m-%dT%H:%M:%S')
        # when
        response = await async_client.get(
            f'{report_router_url}/week?date={today}',
            headers={'account': '1'}
        )
    # then
    result = response.json()
    assert_that(response.status_code).is_equal_to(400)
    assert_that(result['body']).is_equal_to(REPORT_NOT_FOUND)


@maintain_idempotent_async()
async def test_월_리포트_조회(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    # given
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

    with freezegun.freeze_time('2022-02-01'):
        # when
        await async_client.post(
            f'{report_batch_router_url}/month?account-id=1'
        )
        today = get_start_datetime(get_now()).strftime('%Y-%m-%dT%H:%M:%S')
        # when
        response = await async_client.get(
            f'{report_router_url}/month?date={today}',
            headers={'account': '1'}
        )
        assert_that(response.status_code).is_equal_to(200)
        result = response.json()
        message = result['message']
        assert_that(message['status']).is_equal_to(HttpStatus.REPORT_DETAIL_OK.value)
        data = result['data']
        assert_that(data).contains_key('account_id', 'category_detail', 'category_routine_count', 'created_at', 'weekly_achievement_rate')
        category_detail = data['category_detail']
        assert_that(category_detail).contains_key('DAILY', 'ETC', 'HEALTH', 'MIRACLE', 'SELF')
        weekly_achievement_rate = data['weekly_achievement_rate']
        assert_that(len(weekly_achievement_rate)).is_equal_to(4)


@maintain_idempotent_async()
async def test_월_리포트_없을_때_조회(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
    with freezegun.freeze_time('2022-02-01'):
        today = get_start_datetime(get_now()).strftime('%Y-%m-%dT%H:%M:%S')
        # when
        response = await async_client.get(
            f'{report_router_url}/month?date={today}',
            headers={'account': '1'}
        )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json()['body']).is_equal_to(REPORT_NOT_FOUND)
