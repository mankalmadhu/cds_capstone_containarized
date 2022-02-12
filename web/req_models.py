from datetime import datetime
from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel


class AutoName(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class Operations(AutoName):
    fetch = auto()
    clean = auto()
    feature_extract = auto()
    label = auto()
    model_train = auto()
    model_test = auto()
    produce_tweet = auto()
    stream_predict = auto()


class TaskBaseModel(BaseModel):
    operation: Operations = None
    save: Optional[bool] = False
    verbose: Optional[bool] = False


class FetchDataModel(TaskBaseModel):
    fetch_date: Optional[datetime] = None
    total_tweets_to_fetch: Optional[int] = 0
