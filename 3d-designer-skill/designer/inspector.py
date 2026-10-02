"""INSPECT phase: mesh sanity + printability + design assertions.

Mesh checks (trimesh):   watertight, consistent winding, positive volume, bounding box vs print bed,
                         overhang area estimate (faces pointing down steeper than the overhang angle),
                         thin-feature estimate from the mesh's smallest bounding-box extent per component.
Design checks (plan):    every expression in plan["checks"] is evaluated against the CHECK variables
                         the model echoes, plus any `ok=false` echoed by the model itself.
Output: build/inspection.json + build/inspection.md.  Exit status 1 when any check fails.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from .project import Project

OVERHANG_DEG = 50.0


def _mesh_report(stl: Path, bed: list[float], min_wall: float) -> dict:
    import trimesh
    m = trimesh.load(stl, force="mesh")
    r = {"file": stl.name, "faces": int(len(m.faces)), "watertight": bool(m.is_watertight),
         "winding_consistent": bool(m.is_winding_consistent), "volume_mm3": float(round(m.volume, 1)),
         "extents_mm": [round(float(x), 2) for x in m.extents], "components": int(len(m.split(only_watertight=False))),
         "issues": []}
    if not r["watertight"]:
        r["issues"].append("mesh is not watertight (slicer may fail or fill incorrectly)")
    if r["volume_mm3"] <= 0:
        r["issues"].append("non-positive volume: inverted normals or degenerate geometry")
    ext = sorted(m.extents)
    bed_sorted = sorted(bed)
    if not (ext[0] <= bed_sorted[0] + 1e-6 and ext[1] <= bed_sorted[1] + 1e-6 and ext[2] <= bed_sorted[2] + 1e-6):
        r["issues"].append(f"part {r['extents_mm']} exceeds print bed {bed} — split it or shrink it")
    # overhang estimate: down-facing faces not on the bottom plane
    n = m.face_normals
    z0 = m.bounds[0][2]
    centers = m.triangles_center
    down = (n[:, 2] < -math.cos(math.radians(90 - OVERHANG_DEG))) & (centers[:, 2] > z0 + 0.3)
    area = m.area_faces
    frac = float(area[down].sum() / area.sum()) if area.sum() > 0 else 0.0
    r["overhang_area_fraction"] = round(frac, 3)
    if frac > 0.15:
        r["issues"].append(f"{frac:.0%} of surface area overhangs > {OVERHANG_DEG:.0f}°: re-orient or add supports")
    elif frac > 0.03:
        r["notes"] = [f"{frac:.0%} of surface overhangs; small bridges/chamfers are probably fine"]
    # thin components (e.g. a stray sliver)
    thin = []
    for c in m.split(only_watertight=False):
        e = sorted(c.extents)
        if e[0] < min_wall and c.volume < 50:
            thin.append([round(float(x), 2) for x in c.extents])
    if thin:
        r["issues"].append(f"{len(thin)} tiny/thin fragment(s) in the mesh (extents {thin[:3]}) — likely a modelling slip")
    return r


def _volume(stl: Path) -> float:
    import trimesh
    if stl.stat().st_size < 64:
        return 0.0
    m = trimesh.load(stl, force="mesh")
    return float(abs(m.volume)) if len(m.faces) else 0.0


def _eval_check(expr: str, env: dict) -> tuple[bool, str]:
    safe = {"abs": abs, "min": min, "max": max, "sqrt": math.sqrt, "pi": math.pi, "true": True, "false": False}
    try:
        val = eval(expr, {"__builtins__": {}}, {**safe, **env})   # noqa: S307 — plan.json is authored by the user
        return bool(val), ""
    except Exception as e:  # missing variable etc.
        return False, f"{type(e).__name__}: {e}"


def inspect(project: Project) -> dict:
    plan = project.plan
    manifest = project.read_json("manifest.json")
    if not manifest:
        raise SystemExit("no build/manifest.json — run `designer build` first")
    bed = plan.get("constraints", {}).get("print_bed_mm", [220, 220, 250])
    min_wall = plan.get("constraints", {}).get("min_wall_mm", 1.6)
    report = {"meshes": [], "design_checks": [], "failures": [], "warnings": list(manifest.get("warnings", []))}
    for name, info in manifest["parts"].items():
        stl = Path(info["stl"])
        if not info.get("ok") or not stl.exists():
            report["failures"].append(f"{name}: did not compile")
            continue
        if info.get("must_be_empty"):
            vol = _volume(stl)
            ok = vol < 0.5
            report["design_checks"].append({"expr": f"{name} has no interference (volume {vol:.2f} mm³)", "ok": ok, "error": ""})
            if not ok:
                report["failures"].append(f"{name}: parts intersect — {vol:.1f} mm³ of overlap in the assembled position")
            continue
        mr = _mesh_report(stl, bed, min_wall)
        report["meshes"].append(mr)
        report["failures"] += [f"{name}: {i}" for i in mr["issues"]]
    env = dict(manifest.get("checks", {}))
    for k, v in env.items():
        if k == "ok" and v is False:
            report["failures"].append("model echoed ok=false in a CHECK line")
    for expr in plan.get("checks", []):
        ok, err = _eval_check(expr, env)
        report["design_checks"].append({"expr": expr, "ok": ok, "error": err})
        if not ok:
            report["failures"].append(f"design check failed: {expr} {err}")
    report["ok"] = not report["failures"]
    report["check_values"] = env
    project.write_json("inspection.json", report)
    (project.build_dir / "inspection.md").write_text(render_md(report))
    return report


def render_md(r: dict) -> str:
    lines = [f"# Inspection report — {'PASS' if r['ok'] else 'FAIL'}", ""]
    lines += ["| part | watertight | volume mm³ | extents mm | overhang | issues |", "|---|---|---|---|---|---|"]
    for m in r["meshes"]:
        lines.append(f"| {m['file']} | {'yes' if m['watertight'] else 'NO'} | {m['volume_mm3']:.0f} | {m['extents_mm']} | {m['overhang_area_fraction']:.0%} | {'; '.join(m['issues']) or '—'} |")
    lines += ["", "## Design checks", ""]
    for c in r["design_checks"]:
        lines.append(f"- {'✅' if c['ok'] else '❌'} `{c['expr']}` {c['error']}")
    if r["check_values"]:
        lines += ["", "## Values echoed by the model", ""]
        lines += [f"- {k} = {v}" for k, v in r["check_values"].items()]
    if r["warnings"]:
        lines += ["", "## Compiler warnings", ""] + [f"- {w}" for w in r["warnings"]]
    if r["failures"]:
        lines += ["", "## Failures", ""] + [f"- {f}" for f in r["failures"]]
    return "\n".join(lines) + "\n"
