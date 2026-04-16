"""Top-level package for py.draw.io."""
from py_draw_io.cache import CacheFile
from py_draw_io.settings import Settings

SETTINGS = Settings()
EXPORT_CACHE = CacheFile.load(create_if_necessary=True)
