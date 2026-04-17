import datetime
import json
import shutil

import pytest
from pydantic import ValidationError

from py_draw_io import CacheFile
from py_draw_io.cache import FileCache, CacheValidationError


def test_file_cache_new(tmp_path):
    cache = FileCache.new("yolo")
    assert cache.hash == "yolo"
    assert cache.files == []


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
    with open(tmp_file, "w") as file_p:
        file_p.write("{}")
    with pytest.raises(ValidationError):
        CacheFile.load(tmp_file)


def test_load_success(tmp_path):
    tmp_file = tmp_path / "file.json"
    created = datetime.datetime.now()
    updated = datetime.datetime.now() + datetime.timedelta(days=1)
    with open(tmp_file, "w") as file_p:
        json.dump({
            "created": created.isoformat(),
            "updated": updated.isoformat(),
            "files": {}
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


def test_check_file(tmp_path):
    source1 = tmp_path / "source1.json"
    with open(source1, "w") as file_p:
        file_p.write("yolo")

    source2 = tmp_path / "source2.json"
    with open(source1, "w") as file_p:
        file_p.write("yolo2")

    target1 = tmp_path / "target1.png"
    target2 = tmp_path / "target2.png"

    cache_file = tmp_path / "cache.json"
    with open(cache_file, "w") as file_p:
        json.dump({
            "created": "2026-04-17T08:06:20.412456",
            "updated": "2026-04-17T08:06:20.412526",
            "files": {
                source1.as_posix(): {
                    "hash": "d35de2bb4264afdf24b3f94b71848db0a8b799246e7620f2aca5ddf3d91438d2",
                    "files": [
                        target1.as_posix()
                    ]
                }
            }
        }, file_p)

    cache = CacheFile.load(cache_file)
    cache.check_file(source1, target1)

    with pytest.raises(CacheValidationError):
        cache.check_file(source2, target1)

    with pytest.raises(CacheValidationError):
        cache.check_file(source1, target2)

    with pytest.raises(CacheValidationError):
        cache.check_file(source2, target2)
