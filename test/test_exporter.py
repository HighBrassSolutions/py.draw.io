import os
import shutil
from pathlib import Path

import pytest

from py_draw_io.exporter import DrawIoExporter, IllegalExtensionError

FILE_FOR_TEST_PATH = Path(__file__).parent / "test_diagram.drawio"


@pytest.fixture
def export_temp():
    temp_dir = Path("temp")
    os.makedirs(temp_dir, exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_file_not_found(tmp_path):
    out_path = tmp_path / "out.png"
    assert not out_path.is_file()

    with pytest.raises(FileNotFoundError):
        DrawIoExporter().export(Path("temp/not_existent.drawio"), "test", out_path, None)
    assert not out_path.is_file()


def test_illegal_extension(tmp_path):
    out_path = tmp_path / "out.png"
    assert not out_path.is_file()

    input_file = tmp_path / "diag.html"
    with open(input_file, "w") as file_p:
        file_p.write("nothing")

    with pytest.raises(IllegalExtensionError):
        DrawIoExporter().export(input_file, "test", out_path, None)
    assert not out_path.is_file()


def test_default_file_name(export_temp):
    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert not files

    DrawIoExporter().export(FILE_FOR_TEST_PATH, "pagerino", None, None)

    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert len(files) == 1
    assert files[0].suffix == ".png"
    assert "pagerino" in files[0].name


def test_default_file_name_with_limit(export_temp):
    limit_geo = "eERzdUeXhqdjQ1jmuvG7-1"
    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert not files

    DrawIoExporter().export(FILE_FOR_TEST_PATH, "pagerino", None, limit_geo)

    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert len(files) == 1
    assert files[0].suffix == ".png"
    assert "pagerino" in files[0].name
    assert limit_geo in files[0].name
