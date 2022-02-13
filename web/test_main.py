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


def test_model_test_task_e2e():

    json_str = '{"operation":"model_test", "verbose": true}'

    response = client.post("/tasks/model_test", json=json.loads(json_str))

    content = response.json()
    task_id = content["task_id"]
    assert task_id

    response = client.get(f"tasks/{task_id}")
    content = response.json()
    assert content == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None
    }
    assert response.status_code == 200

    while content["task_status"] == "PENDING":
        response = client.get(f"tasks/{task_id}")
        content = response.json()

    assert content == {
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": True
    }
