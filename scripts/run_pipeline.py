"""CLI entry-point to execute the full macro analytics pipeline."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from inflation_tracker.pipeline import run_pipeline  # noqa: E402

if __name__ == "__main__":
    run_pipeline(PROJECT_ROOT)
    print("Pipeline completed successfully.")
