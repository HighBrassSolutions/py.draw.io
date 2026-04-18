import os
import shutil
from pathlib import Path
from typing import Optional

import pytest
import datetime

from py_draw_io import SETTINGS

SETTINGS.use_cache = False


class Timer:
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]

    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = datetime.datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()

    @property
    def duration(self) -> datetime.timedelta:
        if self.start is None or self.end is None:
            raise RuntimeError()
        return self.end - self.start


@pytest.fixture()
def temp_dir():
    temp = Path("temp")
    os.makedirs(temp, exist_ok=True)
    yield temp
    shutil.rmtree(temp)
