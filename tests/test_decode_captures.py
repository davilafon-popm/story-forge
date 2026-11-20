import base64
import io
import json
import subprocess
import sys
import zipfile

from conftest import SCRIPTS
from PIL import Image


def _png(color, size):
    b = io.BytesIO()
    Image.new("RGB", size, color).save(b, "PNG")
    return b.getvalue()


def _run(tmp_path, *files, sheet=False):
    out = tmp_path / "out"
    cmd = [sys.executable, "-I", str(SCRIPTS / "decode_captures.py"), "--output", str(out)]
    if sheet:
        cmd.append("--contact-sheet")
    r = subprocess.run(cmd + [str(f) for f in files], capture_output=True, text=True)
    return r, out


def test_png_from_json_result(tmp_path):
    f = tmp_path / "r1.json"
    f.write_text(json.dumps([{"type": "text", "text": "@@01-a@@" + base64.b64encode(_png("red", (39, 84))).decode()}]))
    r, out = _run(tmp_path, f, sheet=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert Image.open(out / "01-a.png").size == (39, 84)
    assert (out / "_contact-sheet.png").exists()


def test_zip_keeps_largest_png(tmp_path):
    z = io.BytesIO()
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("a@1x.png", _png("blue", (10, 10)))
        zf.writestr("a@2x.png", _png("blue", (20, 20)))
    f = tmp_path / "r2.txt"
    f.write_text("@@02-zip@@" + base64.b64encode(z.getvalue()).decode())
    r, out = _run(tmp_path, f)
    assert r.returncode == 0
    assert Image.open(out / "02-zip.png").size == (20, 20)


def test_truncated_image_fails(tmp_path):
    good = base64.b64encode(_png("green", (30, 30))).decode()
    f = tmp_path / "r3.txt"
    f.write_text("@@03-bad@@" + good[: len(good) // 2])
    r, _ = _run(tmp_path, f)
    assert r.returncode == 1
    assert "FAILED 03-bad" in r.stdout


def test_spanish_aliases_still_work(tmp_path):
    f = tmp_path / "r4.txt"
    f.write_text("@@04-alias@@" + base64.b64encode(_png("white", (5, 5))).decode())
    out = tmp_path / "salida"
    r = subprocess.run([sys.executable, "-I", str(SCRIPTS / "decode_captures.py"), "--salida", str(out), str(f)],
                       capture_output=True, text=True)
    assert r.returncode == 0 and (out / "04-alias.png").exists()
