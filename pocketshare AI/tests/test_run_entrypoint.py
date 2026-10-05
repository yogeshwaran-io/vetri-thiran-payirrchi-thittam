import importlib.util
from pathlib import Path


def test_run_module_exposes_main_entrypoint():
    root = Path(__file__).resolve().parents[1]
    module_path = root / "run.py"

    assert module_path.exists()

    spec = importlib.util.spec_from_file_location("project_run", module_path)
    assert spec is not None and spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(module.main)
