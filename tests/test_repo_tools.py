import subprocess
import sys

from conftest import ROOT


def _run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(ROOT / "tools" / script), *args], capture_output=True, text=True, cwd=cwd)


def test_plugin_is_valid():
    r = _run("validate_plugin.py")
    assert r.returncode == 0, r.stdout


def test_references_resolve():
    r = _run("check_references.py")
    assert r.returncode == 0, r.stdout


def test_repository_has_no_sensitive_data():
    r = _run("sanitize_check.py", "--root", str(ROOT))
    assert r.returncode == 0, r.stdout


def test_sanitize_detects_planted_secret(tmp_path):
    leak = "site acme." + "atlassian.net token figd_" + "abcdefghijklmnop1234\n"  # built at runtime; sanitize: allow
    (tmp_path / "leak.md").write_text(leak)
    r = _run("sanitize_check.py", "--root", str(tmp_path))
    assert r.returncode == 1
    assert "atlassian site" in r.stdout and "token-like secret" in r.stdout


def test_sanitize_uses_private_denylist(tmp_path):
    (tmp_path / "a.md").write_text("Built for Contoso Bank.\n")
    (tmp_path / ".sanitize-denylist").write_text("contoso\n")
    r = _run("sanitize_check.py", "--root", str(tmp_path))
    assert r.returncode == 1 and "denylist term" in r.stdout
