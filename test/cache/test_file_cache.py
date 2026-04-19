from py_draw_io.cache import FileCache


def test_new(tmp_path):
    cache = FileCache.new("yolo")
    assert cache.hash == "yolo"
    assert cache.files == []
