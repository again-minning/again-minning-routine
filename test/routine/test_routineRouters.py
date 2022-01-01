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
        'days': [1, 2, 3]
    }
    response = client.request('post', '/api/v1/routine/create', json=request)
    assert_that(response.status_code).is_not_equal_to('200')
