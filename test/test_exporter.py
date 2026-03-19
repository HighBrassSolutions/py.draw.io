import os
import shutil
from pathlib import Path

import pytest

from py_draw_io.exporter import DrawIoExporter, IllegalExtensionError, ExportFailedError

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


def test_file_already_present(tmp_path):
    out_path = tmp_path / "out.png"

    with open(out_path, "w") as file_p:
        file_p.write("")
    assert out_path.stat().st_size < 5

    DrawIoExporter().export(FILE_FOR_TEST_PATH, "pagerino", out_path, None)

    assert out_path.stat().st_size > 9000


def test_export_failure(export_temp):
    test_data = """
    <mxfyle host="Electron" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/29.6.1 Chrome/142.0.7444.265 Electron/39.8.0 Safari/537.36" version="29.6.1" pages="4">
      <diagram id="69C91-wjoXnYqn4PnUJh" name="pagerino">
        <mxGraphModel dx="1412" dy="1018" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
          <root>
            <mxCell id="0" />
            <mxCell id="1" parent="0" />
            <mxCell id="eERzdUeXhqdjQ1jmuvG7-3" edge="1" parent="1" source="eERzdUeXhqdjQ1jmuvG7-1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;">
              <mxGeometry relative="1" as="geometry">
                <Array as="points">
                  <mxPoint x="330" y="180" />
                  <mxPoint x="330" y="200" />
                </Array>
                <mxPoint x="400" y="280" as="targetPoint" />
              </mxGeometry>
            </mxCell>
            <mxCell id="eERzdUeXhqdjQ1jmuvG7-1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;" value="" vertex="1">
              <mxGeometry height="60" width="120" x="140" y="150" as="geometry" />
            </mxCell>
            <mxCell id="eERzdUeXhqdjQ1jmuvG7-2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;" value="" vertex="1">
              <mxGeometry height="60" width="120" x="450" y="160" as="geometry" />
          </root>
        </mxGraphModel>
      </diagram>
    </mxfile>
    """
    dummy_file = export_temp / "dummy.drawio"
    with open(dummy_file, "w") as file_p:
        file_p.write(test_data)

    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert len(files) == 1

    with pytest.raises(ExportFailedError):
        DrawIoExporter().export(dummy_file, "pagerino", None, None)

    files = [x for x in export_temp.iterdir() if x.is_file()]
    assert len(files) == 1


def test_success(tmp_path):
    out_path = tmp_path / "out.png"

    DrawIoExporter().export(FILE_FOR_TEST_PATH, "pagerino", out_path, None)

    assert out_path.stat().st_size > 9000

    DrawIoExporter().export(FILE_FOR_TEST_PATH, "pagerino", out_path, "eERzdUeXhqdjQ1jmuvG7-2")

    print(out_path.stat().st_size)
    assert out_path.stat().st_size < 3000