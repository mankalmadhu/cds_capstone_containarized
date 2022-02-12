from fastapi.testclient import TestClient
from celery.result import AsyncResult

from main import app

client = TestClient(app)


def test_run_fetch_task(mocker):
    wroker_mock = mocker.patch('worker.create_task.delay',
                               return_value=AsyncResult(id='1234'))

    response = client.post("/tasks/fetch_data",
                           json={
                               "operation": "fetch",
                               "save": True
                           })

    wroker_mock.assert_called_once_with(['--operation fetch', '--save True'])

    assert response.json() == {"task_id": '1234'}