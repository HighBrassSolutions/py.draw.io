import json
import pytest

from py_draw_io.cache import CacheValidationError, CacheFile


def test_check_file(tmp_path):
    source1 = tmp_path / "source1.json"
    with open(source1, "w") as file_p:
        file_p.write("yolo")

    source2 = tmp_path / "source2.json"
    with open(source2, "w") as file_p:
        file_p.write("yolo2")

    target1 = tmp_path / "target1.png"
    target2 = tmp_path / "target2.png"

    cache_file = tmp_path / "cache.json"
    with open(cache_file, "w") as file_p:
        json.dump({
            "created": "2026-04-17T08:06:20.412456",
            "updated": "2026-04-17T08:06:20.412526",
            "files": {
                source2.as_posix(): {
                    "hash": "d35de2bb4264afdf24b3f94b71848db0a8b799246e7620f2aca5ddf3d91438d2",
                    "files": [
                        target1.as_posix()
                    ]
                }
            }
        }, file_p)

    cache = CacheFile.load(cache_file)
    cache.check_file(source2, target1)

    with pytest.raises(CacheValidationError):
        cache.check_file(source1, target1)

    with pytest.raises(CacheValidationError):
        cache.check_file(source2, target2)

    with pytest.raises(CacheValidationError):
        cache.check_file(source1, target2)


def test_check_file_hash_does_not_match(tmp_path):
    source1 = tmp_path / "source1.json"
    with open(source1, "w") as file_p:
        file_p.write("yolo")

    target1 = tmp_path / "target1.png"

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
    with pytest.raises(CacheValidationError):
        cache.check_file(source1, target1)


def test_check_file_does_not_exist(tmp_path):
    source1 = tmp_path / "source1.json"
    target1 = tmp_path / "target1.png"

    cache = CacheFile.new()
    with pytest.raises(FileNotFoundError):
        cache.check_file(source1, target1)
