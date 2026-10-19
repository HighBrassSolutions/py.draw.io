import json

import pytest

from py_draw_io.cache import CacheFile


def test_file_not_found(tmp_path):
    source1 = tmp_path / "source1.json"
    target1 = tmp_path / "target1.png"

    cache = CacheFile.new()
    with pytest.raises(FileNotFoundError):
        cache.add_to_cache(source1, target1)


def test_first_add(tmp_path):
    source1 = tmp_path / "source1.json"
    with source1.open("w") as file_p:
        file_p.write("yolo")

    target1 = tmp_path / "target1.png"

    cache = CacheFile.new()
    assert len(cache.files) == 0

    cache.add_to_cache(source1, target1)
    assert len(cache.files) == 1

    cache.add_to_cache(source1, target1)
    assert len(cache.files) == 1


def test_different_hash(tmp_path):
    source1 = tmp_path / "source1.json"
    with source1.open("w") as file_p:
        file_p.write("yolo")

    target1 = tmp_path / "target1.png"

    cache_file = tmp_path / "cache.json"
    with cache_file.open("w") as file_p:
        json.dump({
            "created": "2026-04-17T08:06:20.412456",
            "updated": "2026-04-17T08:06:20.412526",
            "files": {
                source1.as_posix(): {
                    "hash": "yolo123",
                    "files": [
                        target1.as_posix(),
                    ],
                },
            },
        }, file_p)

    cache = CacheFile.load(cache_file)
    assert len(cache.files) == 1
    assert cache.files[source1.as_posix()].hash == "yolo123"

    cache.add_to_cache(source1, target1)
    assert len(cache.files) == 1
    assert cache.files[source1.as_posix()].hash != "yolo123"
