from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from worker import create_task
from web.req_models import TaskBaseModel, FetchDataModel
from celery.result import AsyncResult

app = FastAPI()


@app.post("/tasks", status_code=201)
def run_task(task_model: TaskBaseModel):
    return JSONResponse({"message": "No Specific Task Asked"})


@app.post("/tasks/fetch_data", status_code=201)
def run_fetch_task(task_model: FetchDataModel):

    command_options = [
        f'--{k} {v}' for k, v in task_model.dict().items()
        if v and k != 'operation'
    ]

    command_options.insert(0, f'--operation {task_model.operation.name}')

    task = create_task.delay(command_options)
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):

    task_result = AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
