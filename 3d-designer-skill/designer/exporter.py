"""EXPORT phase: emit each part in the requested formats.

OpenSCAD handles: stl, off, amf, 3mf, csg, dxf/svg (2-D projection), png (rendered preview).
trimesh handles:  obj, ply, glb, gltf, 3mf (fallback), stl-binary.
STEP is not produced here (OpenSCAD has no B-rep); see docs/EXPORT_FORMATS.md for the CadQuery route.
"""
from __future__ import annotations
import shutil, subprocess
from pathlib import Path
from .project import Project
from .builder import run_openscad, openscad_bin

SCAD_FORMATS = {"stl", "off", "amf", "3mf", "csg"}
TRIMESH_FORMATS = {"obj", "ply", "glb", "gltf", "3mf", "stl"}
FLAT_FORMATS = {"dxf", "svg"}


def _png(model: Path, out: Path, part: str, camera: str, size="1200,900") -> dict:
    extra = [f"--camera={camera}", "--projection=o", f"--imgsize={size}", "--colorscheme=Tomorrow", "--autocenter", "--viewall"]
    cmd_prefix = []
    if shutil.which("xvfb-run"):
        cmd_prefix = ["xvfb-run", "-a"]
    cmd = cmd_prefix + [openscad_bin(), "-o", str(out), "-D", f'part="{part}"'] + extra + [str(model)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return {"ok": p.returncode == 0 and out.exists(), "cmd": " ".join(cmd)}


def export(project: Project, formats: list[str] | None = None, parts: list[str] | None = None) -> dict:
    plan = project.plan
    model = project.model
    formats = [f.lower() for f in (formats or plan.get("exports", ["stl"]))]
    out_dir = project.build_dir / "export"
    out_dir.mkdir(exist_ok=True)
    result = {}
    names = [p["name"] for p in plan.get("parts", []) if p.get("printable", True) and (not parts or p["name"] in parts)]
    views = plan.get("views", [{"name": "assembly", "part": "assembly", "camera": "0,0,25,55,0,35,520"}])
    for fmt in formats:
        if fmt == "png":
            for v in views:
                out = out_dir / f"{v['name']}.png"
                r = _png(model, out, v["part"], v.get("camera", "0,0,0,55,0,25,500"))
                result[f"{v['name']}.png"] = r["ok"]
                print(f"  [{'ok' if r['ok'] else 'FAIL'}] {out.name}")
            continue
        for name in names:
            out = out_dir / f"{name}.{fmt}"
            try:
                r = _export_one(project, model, name, fmt, out)
            except Exception as e:  # keep going; the summary shows what failed
                r = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            result[out.name] = r.get("ok", False)
            print(f"  [{'ok' if r.get('ok') else 'FAIL'}] {out.name}" + (f"  {r['error']}" if r.get("error") else ""))
    project.write_json("exports.json", result)
    return result


def _export_one(project: Project, model: Path, name: str, fmt: str, out: Path) -> dict:
    if fmt in FLAT_FORMATS:
        # 2-D silhouette (top-down projection) as DXF/SVG: laser-cut templates, drawings
        import trimesh
        from trimesh.path.polygons import projected
        src = project.build_dir / f"{name}.stl"
        if not src.exists():
            run_openscad(model, src, {"part": name})
        m = trimesh.load(src, force="mesh")
        poly = projected(m, normal=[0, 0, 1])
        path = trimesh.load_path(poly)
        path.export(str(out), file_type=fmt)
        r = {"ok": out.exists()}
    elif fmt in SCAD_FORMATS and fmt != "stl":
        r = run_openscad(model, out, {"part": name})
    elif fmt == "stl":
        src = project.build_dir / f"{name}.stl"
        if src.exists():
            shutil.copy(src, out); r = {"ok": True}
        else:
            r = run_openscad(model, out, {"part": name})
    elif fmt in TRIMESH_FORMATS:
        import trimesh
        src = project.build_dir / f"{name}.stl"
        if not src.exists():
            run_openscad(model, src, {"part": name})
        m = trimesh.load(src, force="mesh")
        m.export(str(out), file_type=fmt)
        r = {"ok": out.exists()}
    else:
        r = {"ok": False, "error": f"unknown format {fmt}"}
    return r
