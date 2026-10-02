"""Project layout helpers.  A project is a folder with spec.md, plan.json, a .scad model and build/."""
from __future__ import annotations
import json, os, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "designer" / "knowledge"


class Project:
    def __init__(self, path: str | os.PathLike):
        self.dir = Path(path).resolve()
        self.spec = self.dir / "spec.md"
        self.plan_file = self.dir / "plan.json"
        self.build_dir = self.dir / "build"
        self.build_dir.mkdir(parents=True, exist_ok=True)

    @property
    def plan(self) -> dict:
        if not self.plan_file.exists():
            raise SystemExit(f"no plan.json in {self.dir} — run `designer plan` first")
        return json.loads(self.plan_file.read_text())

    def save_plan(self, plan: dict) -> None:
        self.plan_file.write_text(json.dumps(plan, indent=2) + "\n")

    @property
    def model(self) -> Path:
        return self.dir / self.plan.get("model", "model.scad")

    def write_json(self, name: str, data) -> Path:
        p = self.build_dir / name
        p.write_text(json.dumps(data, indent=2, default=str) + "\n")
        return p

    def read_json(self, name: str, default=None):
        p = self.build_dir / name
        return json.loads(p.read_text()) if p.exists() else default


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def lap(self) -> float:
        now = time.time(); d = now - self.t0; self.t0 = now
        return round(d, 2)
