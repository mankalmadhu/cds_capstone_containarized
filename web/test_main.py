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

    wroker_mock.assert_called_once_with(" ".join([
        '--operation fetch',
        '--params \'{"save": true, "verbose": false, "fetch_date": null, "total_tweets_to_fetch": 0}\''
    ]))

    assert response.json() == {"task_id": '1234'}


def progress_checker(uri, json_body_str):
    response = client.post(uri, json=json.loads(json_body_str))

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


def test_model_test_task_e2e():

    json_str = '{"verbose": true}'
    progress_checker("/tasks/model_test", json_str)


def test_feature_extract_task():

    json_str = '{"verbose": true}'
    progress_checker("/tasks/extract_features", json_str)


def test_model_train_task():

    json_str = '{"verbose": true, "ml_model":"naive_bayes", "features": ["idf_features", "cv_features"]}'
    progress_checker("/tasks/train_model", json_str)
