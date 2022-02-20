from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from ml_boms import Operations


class TaskBaseModel(BaseModel):
    save: Optional[bool] = False
    verbose: Optional[bool] = False


class FetchDataModel(TaskBaseModel):
    fetch_date: Optional[datetime] = None
    total_tweets_to_fetch: Optional[int] = 0
