"""PLATE phase: arrange the printable parts on the target printer's bed and write one 3MF per plate.

A simple shelf packer (largest footprint first) with a margin from the bed edge and a gap between
parts.  Parts that do not fit on one plate spill onto the next.  Output: build/plates/plate_1.3mf ...
plus plates.json describing what is where.  The 3MF is a plain multi-object file, which Bambu Studio,
PrusaSlicer, OrcaSlicer and Cura all import with the objects already positioned.
"""
from __future__ import annotations
import json
from pathlib import Path
from .project import Project


def _load(stl: Path):
    import trimesh
    m = trimesh.load(stl, force="mesh")
    m.apply_translation(-m.bounds[0])          # corner at the origin, sitting on z = 0
    return m


def pack(project: Project, copies: dict[str, int] | None = None) -> dict:
    plan = project.plan
    printer = plan.get("printer", {"name": "generic", "bed_mm": plan["constraints"].get("print_bed_mm", [220, 220, 250])})
    bed_x, bed_y, bed_z = printer["bed_mm"]
    margin, gap = printer.get("margin_mm", 5), printer.get("gap_mm", 6)
    manifest = project.read_json("manifest.json") or {}
    items = []
    for p in plan["parts"]:
        if not p.get("printable", True) or p.get("optional"):
            continue
        stl = Path(manifest.get("parts", {}).get(p["name"], {}).get("stl", project.build_dir / f"{p['name']}.stl"))
        if not stl.exists():
            continue
        for i in range((copies or {}).get(p["name"], p.get("copies", 1))):
            m = _load(stl)
            if m.extents[2] > bed_z or min(m.extents[:2]) > max(bed_x, bed_y):
                raise SystemExit(f"{p['name']} does not fit the bed at all")
            if m.extents[0] < m.extents[1] and m.extents[1] > bed_x - 2 * margin:   # rotate if it only fits the other way
                import trimesh
                m.apply_transform(trimesh.transformations.rotation_matrix(1.5708, [0, 0, 1]))
                m.apply_translation(-m.bounds[0])
            items.append((p["name"], m))
    items.sort(key=lambda t: -(t[1].extents[0] * t[1].extents[1]))
    plates, plate, cur_x, cur_y, row_h = [], [], margin, margin, 0.0
    usable_x, usable_y = bed_x - margin, bed_y - margin
    for name, m in items:
        w, d = m.extents[0], m.extents[1]
        if cur_x + w > usable_x:                       # next row
            cur_x, cur_y, row_h = margin, cur_y + row_h + gap, 0.0
        if cur_y + d > usable_y:                       # next plate
            plates.append(plate); plate, cur_x, cur_y, row_h = [], margin, margin, 0.0
        m.apply_translation([cur_x, cur_y, 0])
        plate.append((name, m, [round(cur_x, 1), round(cur_y, 1)]))
        cur_x += w + gap; row_h = max(row_h, d)
    if plate:
        plates.append(plate)
    out_dir = project.build_dir / "plates"; out_dir.mkdir(exist_ok=True)
    import trimesh
    summary = {"printer": printer, "plates": []}
    for i, pl in enumerate(plates, 1):
        scene = trimesh.Scene()
        for name, m, _ in pl:
            scene.add_geometry(m, node_name=name, geom_name=name)
        # centre the group on the bed
        b = scene.bounds
        shift = [(bed_x - (b[1][0] + b[0][0])) / 2, (bed_y - (b[1][1] + b[0][1])) / 2, 0]
        for node in scene.graph.nodes_geometry:
            T, g = scene.graph[node]
            scene.graph.update(frame_to=node, matrix=trimesh.transformations.translation_matrix(shift) @ T)
        f = out_dir / f"plate_{i}.3mf"
        scene.export(str(f), file_type="3mf")
        summary["plates"].append({"file": str(f), "parts": [{"name": n, "at_mm": at, "size_mm": [round(float(x), 1) for x in m.extents]} for n, m, at in pl]})
        print(f"  plate {i}: {', '.join(n for n, _, _ in pl)}  -> {f.name}")
    project.write_json("plates.json", summary)
    return summary
