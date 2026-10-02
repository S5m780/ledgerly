"""LEARN phase: adaptive memory for the pipeline.

* metrics.jsonl   — one line per run: phase timings, failure counts, iterations.  Used to spot slow phases.
* lessons.json    — tagged, weighted lessons.  The planner injects the best-matching ones into every new plan.
* heuristics.json — tuned defaults (tolerances, clearances) that the planner applies automatically.

`designer learn` is run by the learner agent at the end of every project (and after every failed inspection).
It records metrics automatically; lessons are added with --lesson/--tags, and existing lessons that were
applied and led to a passing build get their weight bumped (reinforcement).
"""
from __future__ import annotations
import json, time
from pathlib import Path
from .project import Project, KNOWLEDGE


def _load(name: str, default):
    p = KNOWLEDGE / name
    return json.loads(p.read_text()) if p.exists() else default


def _save(name: str, data):
    (KNOWLEDGE / name).write_text(json.dumps(data, indent=2) + "\n")


def record_metrics(project: Project, phase_times: dict, iterations: int) -> dict:
    manifest = project.read_json("manifest.json", {})
    insp = project.read_json("inspection.json", {})
    row = {"ts": int(time.time()), "project": project.dir.name, "iterations": iterations, "phase_seconds": phase_times,
           "openscad_seconds": manifest.get("total_seconds"), "parts": len(manifest.get("parts", {})),
           "failures": len(insp.get("failures", [])), "warnings": len(manifest.get("warnings", [])), "passed": insp.get("ok")}
    with (KNOWLEDGE / "metrics.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")
    return row


def add_lesson(lesson: str, tags: list[str], source: str = "", weight: float = 1.0) -> dict:
    lessons = _load("lessons.json", [])
    lid = f"L{len(lessons) + 1:03d}"
    entry = {"id": lid, "lesson": lesson.strip(), "tags": sorted({t.lower() for t in tags} | {"general"} if not tags else {t.lower() for t in tags}),
             "source": source, "weight": weight, "added": time.strftime("%Y-%m-%d")}
    lessons.append(entry)
    _save("lessons.json", lessons)
    with (KNOWLEDGE / "lessons.md").open("a") as f:
        f.write(f"- **{lid}** ({', '.join(entry['tags'])}) — {entry['lesson']}" + (f" _(from {source})_" if source else "") + "\n")
    return entry


def reinforce(project: Project) -> list[str]:
    """Bump the weight of every lesson the plan applied when the inspection passed; decay it when it failed."""
    plan = project.plan
    insp = project.read_json("inspection.json", {})
    lessons = _load("lessons.json", [])
    applied = {l["id"] for l in plan.get("applied_lessons", [])}
    touched = []
    for l in lessons:
        if l["id"] in applied:
            l["weight"] = round(l.get("weight", 1.0) * (1.1 if insp.get("ok") else 0.95), 3)
            touched.append(l["id"])
    _save("lessons.json", lessons)
    return touched


def tune_heuristics(project: Project) -> dict:
    """Fold this project's constraint choices into the running defaults when the build passed."""
    insp = project.read_json("inspection.json", {})
    heur = _load("heuristics.json", {"defaults": {}, "runs": 0})
    if insp.get("ok"):
        c = project.plan.get("constraints", {})
        for k in ("material", "nozzle_mm", "layer_mm", "min_wall_mm"):
            if k in c:
                heur["defaults"][k] = c[k]
        heur["runs"] = heur.get("runs", 0) + 1
    _save("heuristics.json", heur)
    return heur


def summarize_metrics() -> str:
    p = KNOWLEDGE / "metrics.jsonl"
    if not p.exists():
        return "no runs recorded yet"
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    n = len(rows)
    passed = sum(1 for r in rows if r.get("passed"))
    avg_iter = sum(r.get("iterations", 1) for r in rows) / n
    phases = {}
    for r in rows:
        for k, v in (r.get("phase_seconds") or {}).items():
            phases.setdefault(k, []).append(v)
    slow = sorted(((k, sum(v) / len(v)) for k, v in phases.items()), key=lambda x: -x[1])
    lines = [f"runs: {n}, passed first time: {passed}/{n}, mean fix iterations: {avg_iter:.1f}"]
    lines += [f"  avg {k:<10} {s:7.1f}s" for k, s in slow]
    return "\n".join(lines)
