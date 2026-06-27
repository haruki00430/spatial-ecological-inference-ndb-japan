"""Standalone repository path helpers / 単体リポジトリ用パス設定."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_DIR / "config" / "config.yaml"
DATA_RELEASE = PROJECT_DIR / "data" / "release"
DATA_INTERIM = PROJECT_DIR / "02_Data" / "interim"
RESULTS_DIR = PROJECT_DIR / "03_Analysis" / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
GEOJSON_PATH = PROJECT_DIR / "data" / "master" / "japan_prefectures.geojson"
LOG_DIR = PROJECT_DIR / "03_Analysis" / "analysis" / "logs"
HUB_ROOT = PROJECT_DIR.parent.parent


def ensure_ndb_library() -> None:
    """Import ndb_library from pip install or NDB Research Hub src."""
    try:
        import ndb_library  # noqa: F401

        return
    except ImportError:
        pass

    candidates = [
        HUB_ROOT / "src",
        Path.home()
        / ".ag-cursor-common"
        / "research_workspace"
        / "projects"
        / "NDB_Research_Hub"
        / "src",
    ]
    for src in candidates:
        if (src / "ndb_library").is_dir():
            sys.path.insert(0, str(src))
            return

    raise ImportError(
        "ndb_library not found. Clone NDB_Research_Hub and run: "
        "pip install -e /path/to/NDB_Research_Hub"
    )
