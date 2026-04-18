from py_draw_io import Settings
from py_draw_io.cache import FileCache


def test_settings(tmp_path):
    settings = Settings()
    settings.cache_file.files["file_path"] = FileCache.new("yolo")
    assert len(settings.cache_file.files) == 1

    new_cache = tmp_path / "cache.json"
    assert settings.cache_file_location != new_cache

    settings.switch_cache_file(new_cache)
    assert settings.cache_file_location == new_cache
    assert len(settings.cache_file.files) == 0
