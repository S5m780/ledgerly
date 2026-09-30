"""PLAN phase: turn spec.md into a structured plan.json, seeded with lessons from the knowledge base.

The script builds the scaffold (constraints, part list, checks, print settings) so the planner agent
spends its effort on the design decisions, not on boilerplate.  Lessons whose tags overlap the spec's
tags are copied into plan["applied_lessons"] so they are impossible to forget.
"""
from __future__ import annotations
import json, re
from pathlib import Path
from .project import Project, KNOWLEDGE

TEMPLATE = {
    "name": "", "model": "model.scad", "version": 1,
    "goal": "",
    "requirements": [],           # verbatim, testable statements from the spec
    "constraints": {"print_bed_mm": [220, 220, 250], "material": "PETG", "nozzle_mm": 0.4, "layer_mm": 0.2, "min_wall_mm": 1.6},
    "hardware": [],               # off-the-shelf parts with the dimensions the model depends on
    "mechanism": {},              # free-form: ratios, speeds, load paths
    "parts": [],                  # [{"name": "base", "printable": true, "orientation": "..."}]
    "steps": [],                  # ordered build steps, each with a 'done_when'
    "checks": [],                 # assertions over CHECK variables echoed by the model, e.g. "motor_far_radius < inner_r - 1"
    "exports": ["stl", "3mf", "png"],
    "applied_lessons": [],
    "open_questions": [],
}


def parse_spec(text: str) -> dict:
    """Very small front-matter + heading parser: '# key: value' lines and '## Requirements' bullets."""
    out = {"tags": [], "requirements": [], "title": ""}
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        out["title"] = m.group(1).strip()
    tags = re.search(r"^tags:\s*(.+)$", text, re.M | re.I)
    if tags:
        out["tags"] = [t.strip().lower() for t in tags.group(1).split(",") if t.strip()]
    req = re.search(r"^##\s+Requirements\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if req:
        out["requirements"] = [l.strip("-* ").strip() for l in req.group(1).splitlines() if l.strip().startswith(("-", "*"))]
    bed = re.search(r"print[_ ]bed[^0-9]*(\d+)\D+(\d+)\D+(\d+)", text, re.I)
    if bed:
        out["print_bed_mm"] = [int(bed.group(i)) for i in (1, 2, 3)]
    return out


def relevant_lessons(tags: list[str]) -> list[dict]:
    lessons_file = KNOWLEDGE / "lessons.json"
    if not lessons_file.exists():
        return []
    lessons = json.loads(lessons_file.read_text())
    tagset = set(tags)
    scored = []
    for l in lessons:
        overlap = tagset & set(l.get("tags", []))
        if overlap or "general" in l.get("tags", []):
            scored.append((len(overlap), l))
    scored.sort(key=lambda x: (-x[0], -x[1].get("weight", 1)))
    return [l for _, l in scored[:12]]


def make_plan(project: Project, force: bool = False) -> dict:
    if project.plan_file.exists() and not force:
        plan = project.plan
    else:
        plan = json.loads(json.dumps(TEMPLATE))
    spec = parse_spec(project.spec.read_text()) if project.spec.exists() else {"tags": [], "requirements": []}
    plan["name"] = plan.get("name") or spec.get("title") or project.dir.name
    if not plan.get("requirements"):
        plan["requirements"] = spec["requirements"]
    if spec.get("print_bed_mm"):
        plan["constraints"]["print_bed_mm"] = spec["print_bed_mm"]
    heur = json.loads((KNOWLEDGE / "heuristics.json").read_text()) if (KNOWLEDGE / "heuristics.json").exists() else {}
    plan.setdefault("constraints", {}).update({k: v for k, v in heur.get("defaults", {}).items() if k not in plan["constraints"]})
    plan["tags"] = spec["tags"]
    plan["applied_lessons"] = [{"id": l["id"], "lesson": l["lesson"]} for l in relevant_lessons(spec["tags"])]
    project.save_plan(plan)
    return plan
