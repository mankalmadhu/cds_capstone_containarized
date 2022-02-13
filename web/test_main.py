from fastapi.testclient import TestClient
from celery.result import AsyncResult

from main import app
import json

client = TestClient(app)


def test_run_fetch_task(mocker):
    wroker_mock = mocker.patch('worker.create_task.delay',
                               return_value=AsyncResult(id='1234'))

    json_str = '{"operation":"fetch", "save": true}'

    response = client.post("/tasks/fetch_data", json=json.loads(json_str))

    wroker_mock.assert_called_once_with(" ".join(
        ['--operation fetch', '--save ']))

    assert response.json() == {"task_id": '1234'}