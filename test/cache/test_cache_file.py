import datetime
import json

import pytest
from pydantic import ValidationError

from py_draw_io.cache import CacheFile


def test_new(tmp_path):
    start = datetime.datetime.now()
    cache = CacheFile.new()
    end = datetime.datetime.now()
    assert start < cache.created < end
    assert start < cache.updated < end


def test_load_not_found(tmp_path):
    tmp_file = tmp_path / "file.json"
    assert not tmp_file.exists()

    with pytest.raises(FileNotFoundError):
        CacheFile.load(tmp_file)

    _ = CacheFile.load(tmp_file, create_if_necessary=True)


def test_load_decode_error(tmp_path):
    tmp_file = tmp_path / "file.json"
    with tmp_file.open("w") as file_p:
        file_p.write("{}")
    with pytest.raises(ValidationError):
        CacheFile.load(tmp_file)


def test_load_success(tmp_path):
    tmp_file = tmp_path / "file.json"
    created = datetime.datetime.now()
    updated = datetime.datetime.now() + datetime.timedelta(days=1)
    with tmp_file.open("w") as file_p:
        json.dump({
            "created": created.isoformat(),
            "updated": updated.isoformat(),
            "files": {},
        }, file_p)

    cache = CacheFile.load(tmp_file)
    assert cache.files == {}
    assert cache.created == created
    assert cache.updated == updated


def test_save(tmp_path):
    tmp_file = tmp_path / "file.json"
    cache = CacheFile(created=datetime.datetime(year=1990, month=1, day=1),
                      updated=datetime.datetime(year=1990, month=1, day=2),
                      files={})
    before_save = datetime.datetime.now()
    cache.save(tmp_file)
    loaded = CacheFile.load(tmp_file)
    assert loaded.created == datetime.datetime(year=1990, month=1, day=1)
    assert before_save < loaded.updated < datetime.datetime.now()
