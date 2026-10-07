# py.draw.io

Allows for the creation, manipulation and export of draw.io diagrams in python.

py.draw.io reads and writes `.drawio` files as a tree of Python objects (documents, pages, layers and cells), so
diagrams can be generated from code, edited programmatically and exported to images as part of a build.

Its main feature is **exporting only part of a page**: mark a region with a shape and export just the cells that lie
inside it. This lets you keep one large diagram as the single source of truth and still produce separate images for
each section of a document, without maintaining a copy of the diagram per image.

## Features

- Load, modify and save `.drawio` files, including shapes, arrows, layers and multiple pages
- Create new diagrams from scratch
- Export pages to PNG using the draw.io desktop app
- Export only the cells enclosed by a given shape, optionally using dedicated (invisible) marker layers
- Skip exports whose source diagram hasn't changed, using an optional cache

## Installation

py.draw.io requires Python 3.10 or newer. It is not published on PyPI yet, so install it from GitHub:

```shell
pip install git+https://github.com/ShotLab/py.draw.io.git
```

### Installing draw.io

Exporting images additionally requires the [draw.io desktop app](https://github.com/jgraph/drawio-desktop/releases).
Reading, editing and saving diagrams works without it.

| Platform | Command                                                      |
|----------|--------------------------------------------------------------|
| macOS    | `brew install --cask drawio`                                 |
| Windows  | `winget install --id JGraph.Draw --exact`                    |
| Windows  | `choco install drawio`                                       |
| Linux    | `sudo snap install drawio`                                   |
| Linux    | `flatpak install flathub com.jgraph.drawio.desktop`          |

Installers (`.dmg`, `.exe`, `.deb`, `.rpm`, AppImage) are also available on the
[releases page](https://github.com/jgraph/drawio-desktop/releases).

By default, the exporter expects draw.io to be in PATH (`drawio`). On other systems, pass the path to the executable:

```python
from pathlib import Path

from py_draw_io.exporter import DrawIoExporter

exporter = DrawIoExporter(draw_io=Path("/snap/bin/drawio"))
```

Typical locations:

| Installed via         | Executable                                                     |
|-----------------------|----------------------------------------------------------------|
| Windows installer     | `C:\Program Files\draw.io\draw.io.exe`                         |
| `.deb` / `.rpm`       | `/usr/bin/drawio`                                              |
| Snap                  | `/snap/bin/drawio`                                             |
| Flatpak (system-wide) | `/var/lib/flatpak/exports/bin/com.jgraph.drawio.desktop`       |

draw.io is an Electron app and needs a display, even when exporting from the command line. On headless Linux
machines (e.g. CI runners), install `xvfb` and point `draw_io` to a small wrapper script that runs draw.io in a
virtual display:

```shell
#!/bin/sh
exec xvfb-run --auto-servernum /usr/bin/drawio "$@"
```

## Example

Export the area of a diagram that is enclosed by the shape with the ID `frame_backend`:

```python
from pathlib import Path

from py_draw_io.exporter import DrawIoExporter

exporter = DrawIoExporter(marker_layers=["Markers"])
exporter.export(Path("architecture.drawio"), page="Overview", out_path=Path("images/backend.png"),
                limit_export="frame_backend")
```

The documentation explains how to create and edit diagrams, how partial exports decide which cells to keep, and
how the library is structured.

## Documentation

The documentation is built with [MkDocs](https://www.mkdocs.org/). It contains a usage guide, an architecture
overview generated from the code, and an API reference generated from the docstrings:

```shell
poetry install
poetry run mkdocs build --strict   # output in artifacts/docs/
poetry run mkdocs serve            # live preview on http://127.0.0.1:8000
```

## Development

The project uses [Poetry](https://python-poetry.org/). The checks below are the ones run in CI:

```shell
poetry install
poetry run pytest --cov=py_draw_io --cov-branch --cov-fail-under=100
poetry run mypy src/py_draw_io
poetry run ruff check src/py_draw_io
```

The export tests call the draw.io desktop app, so it needs to be installed to run the full test suite.
