"""fig_local.py without a real .fig: synthetic decoded nodes, JSON cache and summary."""
import fig_local


def _nodes():
    G = lambda a, b: {"sessionID": a, "localID": b}  # noqa: E731
    T = lambda x, y: [[1, 0, x], [0, 1, y]]  # noqa: E731
    return [
        {"guid": G(0, 0), "type": "DOCUMENT", "name": "Doc"},
        {"guid": G(0, 1), "type": "CANVAS", "name": "Page 1", "parentIndex": {"guid": G(0, 0), "position": "a"}},
        {"guid": G(1, 1), "type": "SECTION", "name": "Flow", "parentIndex": {"guid": G(0, 1), "position": "a"},
         "size": {"x": 3000, "y": 2000}, "transform": T(0, 0)},
        {"guid": G(1, 2), "type": "FRAME", "name": "Login", "parentIndex": {"guid": G(1, 1), "position": "a"},
         "size": {"x": 390, "y": 844}, "transform": T(0, 0)},
        {"guid": G(1, 3), "type": "TEXT", "name": "t", "parentIndex": {"guid": G(1, 2), "position": "a"},
         "textData": {"characters": "Sign in"}, "transform": T(10, 10)},
        {"guid": G(1, 4), "type": "FRAME", "name": "Web home", "parentIndex": {"guid": G(1, 1), "position": "b"},
         "size": {"x": 1512, "y": 982}, "transform": T(600, 0)},
        {"guid": G(1, 5), "type": "TEXT", "name": "t", "parentIndex": {"guid": G(1, 4), "position": "a"},
         "textData": {"characters": "Welcome"}, "transform": T(10, 10)},
        {"guid": G(1, 6), "type": "FRAME", "name": "Note", "parentIndex": {"guid": G(1, 1), "position": "c"},
         "size": {"x": 200, "y": 100}, "transform": T(0, 1000)},
        {"guid": G(1, 7), "type": "TEXT", "name": "t", "parentIndex": {"guid": G(1, 6), "position": "a"},
         "textData": {"characters": "Max 3 attempts"}, "transform": T(0, 0)},
        {"guid": G(2, 1), "type": "SYMBOL", "name": "Button", "parentIndex": {"guid": G(0, 1), "position": "z"},
         "size": {"x": 10, "y": 10}},
        {"guid": G(1, 8), "type": "INSTANCE", "name": "btn", "parentIndex": {"guid": G(1, 2), "position": "b"},
         "symbolData": {"symbolID": (2, 1), "symbolOverrides": [{"guidPath": [(9, 9)], "visible": True}]},
         "transform": T(10, 100)},
    ]


def test_json_cache_roundtrip_restores_tuples(tmp_path):
    cache = tmp_path / ".cache_x.json.gz"
    fig_local.save_cache(_nodes(), cache)
    loaded = fig_local.load_cache(cache)
    inst = next(n for n in loaded if n["type"] == "INSTANCE")
    assert inst["symbolData"]["symbolID"] == (2, 1)
    assert inst["symbolData"]["symbolOverrides"][0]["guidPath"] == [(9, 9)]
    assert not any(p.suffix == ".pkl" for p in tmp_path.iterdir())


def test_flow_summary_includes_mobile_and_web_screens_and_notes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fig_local, "load", lambda path, outdir: _nodes())
    fig = tmp_path / "app.fig"
    fig.write_bytes(b"")
    fig_local.main(["flow", str(fig), "--node", "1-1", "--output", str(tmp_path / "out")])
    out = capsys.readouterr().out
    assert "2 screens" in out
    assert "Sign in" in out and "Welcome" in out
    assert "Max 3 attempts" in out
    assert (tmp_path / "out" / "app_1-1.md").exists()


def test_spanish_aliases(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fig_local, "load", lambda path, outdir: _nodes())
    fig = tmp_path / "app.fig"
    fig.write_bytes(b"")
    fig_local.main(["flujo", str(fig), "--nodo", "1-1", "--salida", str(tmp_path / "o2")])
    assert "Sign in" in capsys.readouterr().out
