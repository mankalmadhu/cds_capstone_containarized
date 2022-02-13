from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from worker import create_task
from req_models import TaskBaseModel, FetchDataModel
from celery.result import AsyncResult
from operations import Operations

app = FastAPI()


def run_task_base(task_model, operation):

    command_options = [
        f'--operation {operation.name}', '--save' if task_model.save else '',
        '--verbose' if task_model.verbose else ''
    ]

    command_options.extend([
        f'--{k} {v}' for k, v in task_model.dict().items()
        if v and k not in ['save', 'verbose']
    ])

    task = create_task.delay(" ".join(command_options))
    return JSONResponse({"task_id": task.id})


@app.post("/tasks", status_code=201)
def run_task(task_model: TaskBaseModel):
    return JSONResponse({"message": "No Specific Task Asked"})


@app.post("/tasks/fetch_data", status_code=201)
def run_fetch_task(task_model: FetchDataModel):
    return run_task_base(task_model, Operations.fetch)


@app.post("/tasks/clean_data", status_code=201)
def run_clean_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.clean)


@app.post("/tasks/extract_features", status_code=201)
def run_feature_extract_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.feature_extract)


@app.post("/tasks/label", status_code=201)
def run_label_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.label)


@app.post("/tasks/train_model", status_code=201)
def run_train_model_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.model_train)


@app.post("/tasks/model_test", status_code=201)
def run_model_test_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.model_test)


@app.post("/tasks/stream_produce", status_code=201)
def run_stream_produce_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.produce_tweet)


@app.post("/tasks/stream_predict", status_code=201)
def run_stream_predict_task(task_model: TaskBaseModel):
    return run_task_base(task_model, Operations.stream_predict)


@app.get("/tasks/{task_id}")
def get_status(task_id):

    task_result = AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
