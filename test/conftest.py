import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def temp_dir():
    temp = Path("temp")
    os.makedirs(temp, exist_ok=True)
    yield temp
    shutil.rmtree(temp)
