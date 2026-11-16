# py.draw.io

Allows for the creation, manipulation and export of draw.io diagrams in python.

See the **API Reference** in the navigation for the full documentation of every class and function, generated
directly from the source code's docstrings.

## Usage

### Creating a diagram

A diagram is built bottom-up: create a `Layer`, add cells to it, put the layer on a `Diagram` (a page) and the page
into a `Document`, which is then saved as a `.drawio` file.

Cells register themselves with the parent passed to them, so creating a cell with a layer as its parent is enough
to add it to that layer. Cell IDs must be unique within the document, as they are used to reference cells (e.g. as
the source and target of arrows).

```python
from pathlib import Path

from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.diagram import Diagram
from py_draw_io.document import Document
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.graph_model import GraphModel
from py_draw_io.layer import Layer
from py_draw_io.point import Point

layer = Layer(CellCollection(), layer_id="1", name="Content")

client = GeometryCell("client",
                      {"rounded": 1, "whiteSpace": "wrap", "html": 1},
                      "Client",
                      layer,
                      top_left=Point(40, 40),
                      bottom_right=Point(160, 100))
server = GeometryCell("server",
                      {"geometry_type": "ellipse", "whiteSpace": "wrap", "html": 1},
                      "Server",
                      layer,
                      top_left=Point(280, 40),
                      bottom_right=Point(400, 100))
ArrowCell("request",
          {"edgeStyle": "orthogonalEdgeStyle", "html": 1},
          "request",
          layer,
          source=client,
          target=server,
          waypoints=[])

page = Diagram("Overview",
               diagram_id="overview",
               layers=[layer],
               graph_model=GraphModel(grid_size=10,
                                      page_width=850,
                                      page_height=1100))
Document([page], host="py.draw.io", agent="py.draw.io").save(Path("example.drawio"))
```

The style dictionary maps directly to draw.io's style string (`key=value;...`). The special key `geometry_type`
becomes the leading shape name (e.g. `ellipse` or `shape=cylinder3`), and `None` values are written as `none`.
The easiest way to find the right style for a shape is to draw it in draw.io and copy it from
*Edit Style* (Ctrl+E / Cmd+E).

### Editing an existing diagram

Existing files are loaded with `Document.load()`. Pages are looked up by name or ID, and cells by ID, anywhere in
the page including nested children:

```python
document = Document.load(Path("example.drawio"))
page = document.get_diagram("Overview")

server = page.find_by_id("server")
server.value = "API Server"

GeometryCell("database",
             {"geometry_type": "shape=cylinder3", "html": 1},
             "Database",
             server.parent_layer,
             top_left=Point(300, 160),
             bottom_right=Point(380, 240))

document.save(Path("example.drawio"))
```

### Exporting a diagram

`DrawIoExporter` renders a single page of a `.drawio` file into a PNG with a transparent background. It does this by
calling the [draw.io desktop app](https://github.com/jgraph/drawio-desktop/releases), which has to be installed.
By default, the exporter tries to use whatever is in PATH. Pass `draw_io` to use another one:

```python
from py_draw_io.exporter import DrawIoExporter

exporter = DrawIoExporter(draw_io=Path("/usr/bin/drawio"))
exporter.export(Path("example.drawio"), page="Overview", out_path=Path("images/overview.png"), limit_export=None)
```

The source file must have the `.drawio` extension. If `out_path` is `None`, the image is written to the exporter's
`temp_dir` (default `temp/`) as `<page>.png`, or `<page>__<limit_export>.png` when exporting part of a page.

### Exporting part of a diagram

Large diagrams often need to be shown in pieces, for example one image per section of a document. Instead of
maintaining a separate diagram for each piece, you can export just a region of a page by passing the ID of a shape
as `limit_export`. Only cells that lie **completely** inside that shape end up in the image:

- Shapes are kept if both of their corners lie inside the boundary (edges count as inside).
- Arrows are kept if both their source and their target are inside. Waypoints are not checked.
- If a shape is removed, its children are removed with it.

The cleanest way to mark these regions is a **marker layer**: a separate layer containing only invisible frames
(no fill, no stroke) that mark the areas you want to export. Pass the layer's name or ID as `marker_layers` to the
exporter:

```python
document = Document.load(Path("example.drawio"))
page = document.get_diagram("Overview")

markers = Layer(CellCollection(),
                layer_id="markers", 
                ame="Markers")
page.layers.append(markers)
GeometryCell("frame_backend",
             {"fillColor": None, "strokeColor": None},
             None, 
             markers,
             top_left=Point(260, 20),
             bottom_right=Point(420, 260))
document.save(Path("example.drawio"))

exporter = DrawIoExporter(marker_layers=["Markers"])
exporter.export(Path("example.drawio"), page="Overview", out_path=Path("images/backend.png"),
                limit_export="frame_backend")
```

This exports the server and the database, but not the client or the arrow coming from it. When exporting part of a
page, all marker layers are left out except the frame used as the boundary. That frame is kept, so make sure it is
invisible if it shouldn't appear in the image. Whole-page exports (`limit_export=None`) use the file as it is,
including the marker layers, which is why the frames should be invisible.

You can also use any visible shape on a normal layer as the boundary, such as a container or a swimlane. It will
then appear in the exported image as well.

The source file is never modified. The filtered page is written to `temp_dir/diagrams/` and exported from there.

### Caching exports

Exporting through draw.io takes a moment per image. With caching enabled, the exporter remembers a hash of each
source file along with the images exported from it. It skips an export if the image still exists and the source
file is unchanged since that image was exported:

```python
from py_draw_io import SETTINGS

SETTINGS.use_cache = True
```

The cache is stored in `.py_draw_io_cache` in the working directory. It can also be enabled or disabled for a
single exporter with `DrawIoExporter(use_cache=...)`, which takes precedence over the global setting.

## Architecture

A `Document` is a draw.io file. It holds one or more `Diagram`s (the pages), each of which has a `GraphModel` with
the page settings and one or more `Layer`s. Each layer stores its cells in a `CellCollection`.

All diagram elements are `Cell`s. A `GeometryCell` is a shape with a position and size, while an `ArrowCell`
connects two cells or points. Everything that can be checked against a boundary (cells and `Point`s) implements
`Fittable`, and anything that defines a boundary (such as a `GeometryCell`) is a `BoundaryContainer`. Exporting
only part of a diagram relies on this.

`DrawIoExporter` turns a page of a document into an image by calling the draw.io desktop app. If caching is enabled
in the global `Settings`, it records the exported files in a `CacheFile` so that unchanged diagrams are skipped on
the next export.
