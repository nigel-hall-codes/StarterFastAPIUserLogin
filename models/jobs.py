import datetime
from enum import Enum

import pydantic
from typing import Optional

class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    error = "error"