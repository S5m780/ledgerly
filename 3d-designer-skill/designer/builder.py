"""BUILD phase: compile every printable part of the model with OpenSCAD, collecting CHECK echoes,
warnings and timings into build/manifest.json."""
from __future__ import annotations
import re, shutil, subprocess, time
from pathlib import Path
from .project import Project

CHECK_RE = re.compile(r'ECHO: "CHECK (.+)"')
KV_RE = re.compile(r"(\w+)=([^\s]+)")


def openscad_bin() -> str:
    exe = shutil.which("openscad") or shutil.which("openscad-nightly")
    if not exe:
        raise SystemExit("openscad not found on PATH — install it (apt install openscad / brew install openscad)")
    return exe


def run_openscad(model: Path, out: Path, defines: dict | None = None, extra: list[str] | None = None, timeout=900) -> dict:
    cmd = [openscad_bin(), "-o", str(out)]
    for k, v in (defines or {}).items():
        val = f'"{v}"' if isinstance(v, str) else ("true" if v is True else "false" if v is False else str(v))
        cmd += ["-D", f"{k}={val}"]
    cmd += (extra or []) + [str(model)]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    log = p.stdout + p.stderr
    checks = {}
    for m in CHECK_RE.finditer(log):
        for k, v in KV_RE.findall(m.group(1)):
            try:
                checks[k] = float(v)
            except ValueError:
                checks[k] = {"true": True, "false": False}.get(v, v)
    empty = "top level object is empty" in log
    warnings = [l.strip() for l in log.splitlines() if ("WARNING" in l or "ERROR" in l) and "top level object is empty" not in l]
    if empty:
        warnings = []   # an intentionally empty result (interference view) trips the 2-manifold warning
        if not out.exists():
            out.write_text("solid empty\nendsolid empty\n")
    return {"cmd": " ".join(cmd), "ok": p.returncode == 0 and out.exists(), "empty": empty, "seconds": round(time.time() - t0, 2),
            "checks": checks, "warnings": warnings, "log_tail": log[-2000:]}


def build(project: Project, parts: list[str] | None = None) -> dict:
    plan = project.plan
    model = project.model
    if not model.exists():
        raise SystemExit(f"model not found: {model}")
    wanted = [p for p in plan.get("parts", []) if (p.get("printable", True) or p.get("must_be_empty")) and (not parts or p["name"] in parts)]
    manifest = {"model": str(model), "parts": {}, "checks": {}, "warnings": [], "ok": True, "total_seconds": 0.0}
    for p in wanted:
        out = project.build_dir / f"{p['name']}.stl"
        res = run_openscad(model, out, {"part": p["name"], **p.get("defines", {})})
        manifest["parts"][p["name"]] = {"stl": str(out), "must_be_empty": bool(p.get("must_be_empty")), **{k: res[k] for k in ("ok", "seconds", "warnings", "empty")}}
        manifest["checks"].update(res["checks"])
        manifest["warnings"] += [f"{p['name']}: {w}" for w in res["warnings"]]
        manifest["total_seconds"] += res["seconds"]
        manifest["ok"] &= res["ok"]
        print(f"  [{'ok' if res['ok'] else 'FAIL'}] {p['name']:<14} {res['seconds']:6.1f}s  {len(res['warnings'])} warnings")
        if not res["ok"]:
            print(res["log_tail"])
    project.write_json("manifest.json", manifest)
    return manifest
