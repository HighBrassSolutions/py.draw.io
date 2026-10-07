import datetime
import shutil
from pathlib import Path

import pytest

from py_draw_io import SETTINGS

SETTINGS.use_cache = False


class Timer:
    start: datetime.datetime | None
    end: datetime.datetime | None

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
    temp.mkdir(parents=True, exist_ok=True)
    yield temp
    shutil.rmtree(temp)
