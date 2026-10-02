"""designer — command-line front end for the plan -> build -> inspect -> export -> learn loop.

  python -m designer new  <dir> --name "..."          scaffold a project from templates/
  python -m designer plan <dir>                       build/refresh plan.json from spec.md + knowledge
  python -m designer build <dir> [--part p ...]       compile parts with OpenSCAD
  python -m designer inspect <dir>                    mesh + design checks (exit 1 on failure)
  python -m designer export <dir> [--fmt stl 3mf ...] export formats
  python -m designer plate <dir> [--copies part=N]    pack parts onto the printer bed -> build/plates/plate_N.3mf
  python -m designer run <dir> [--max-iter N]         plan+build+inspect (+export when it passes) + metrics
  python -m designer learn <dir> [--lesson ".." --tags a b]   record lessons / reinforce / tune defaults
  python -m designer stats                            what the learner knows
"""
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path
from .project import Project, ROOT, Timer
from . import planner, builder, inspector, exporter, learner, plater


def cmd_new(a):
    d = Path(a.dir); d.mkdir(parents=True, exist_ok=True)
    tpl = ROOT / "templates"
    for src, dst in (("spec.template.md", "spec.md"), ("plan.template.json", "plan.json"), ("model.template.scad", "model.scad")):
        if not (d / dst).exists():
            shutil.copy(tpl / src, d / dst)
    if a.name:
        (d / "spec.md").write_text((d / "spec.md").read_text().replace("<Project title>", a.name))
    print(f"scaffolded {d}")


def cmd_plan(a):
    plan = planner.make_plan(Project(a.dir), force=a.force)
    print(f"plan.json: {len(plan['requirements'])} requirements, {len(plan['parts'])} parts, {len(plan['applied_lessons'])} lessons applied")
    for l in plan["applied_lessons"]:
        print(f"  {l['id']}: {l['lesson']}")


def cmd_build(a):
    m = builder.build(Project(a.dir), a.part)
    print(f"build {'OK' if m['ok'] else 'FAILED'} in {m['total_seconds']:.1f}s, {len(m['warnings'])} warnings")
    sys.exit(0 if m["ok"] else 1)


def cmd_inspect(a):
    r = inspector.inspect(Project(a.dir))
    print((Project(a.dir).build_dir / "inspection.md").read_text())
    sys.exit(0 if r["ok"] else 1)


def cmd_export(a):
    r = exporter.export(Project(a.dir), a.fmt, a.part)
    sys.exit(0 if all(r.values()) else 1)


def cmd_run(a):
    p = Project(a.dir); t = Timer(); times = {}
    planner.make_plan(p); times["plan"] = t.lap()
    ok = False; it = 0
    while it < a.max_iter:
        it += 1
        m = builder.build(p); times["build"] = times.get("build", 0) + t.lap()
        r = inspector.inspect(p) if m["ok"] else {"ok": False, "failures": ["compile failed"]}
        times["inspect"] = times.get("inspect", 0) + t.lap()
        ok = r["ok"]
        print((p.build_dir / "inspection.md").read_text() if m["ok"] else "\n".join(r["failures"]))
        if ok or not a.auto:
            break
        print(f"iteration {it}: {len(r['failures'])} failure(s) — hand back to the builder agent to fix, then re-run")
        break
    if ok:
        exporter.export(p); times["export"] = t.lap()
    learner.record_metrics(p, times, it)
    print(f"run {'PASSED' if ok else 'FAILED'} — phase seconds {times}")
    sys.exit(0 if ok else 1)


def cmd_plate(a):
    copies = dict(kv.split("=") for kv in (a.copies or []))
    plater.pack(Project(a.dir), {k: int(v) for k, v in copies.items()})


def cmd_learn(a):
    p = Project(a.dir)
    if a.lesson:
        e = learner.add_lesson(a.lesson, a.tags or [], source=p.dir.name)
        print(f"recorded {e['id']}")
    touched = learner.reinforce(p)
    heur = learner.tune_heuristics(p)
    print(f"reinforced {touched or 'nothing'}; defaults now {heur.get('defaults')}")


def cmd_stats(a):
    print(learner.summarize_metrics())


def main(argv=None):
    ap = argparse.ArgumentParser(prog="designer", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new"); s.add_argument("dir"); s.add_argument("--name"); s.set_defaults(f=cmd_new)
    s = sub.add_parser("plan"); s.add_argument("dir"); s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_plan)
    s = sub.add_parser("build"); s.add_argument("dir"); s.add_argument("--part", action="append"); s.set_defaults(f=cmd_build)
    s = sub.add_parser("inspect"); s.add_argument("dir"); s.set_defaults(f=cmd_inspect)
    s = sub.add_parser("export"); s.add_argument("dir"); s.add_argument("--fmt", nargs="*"); s.add_argument("--part", action="append"); s.set_defaults(f=cmd_export)
    s = sub.add_parser("run"); s.add_argument("dir"); s.add_argument("--max-iter", type=int, default=3); s.add_argument("--auto", action="store_true"); s.set_defaults(f=cmd_run)
    s = sub.add_parser("plate"); s.add_argument("dir"); s.add_argument("--copies", nargs="*", help="part=N"); s.set_defaults(f=cmd_plate)
    s = sub.add_parser("learn"); s.add_argument("dir"); s.add_argument("--lesson"); s.add_argument("--tags", nargs="*"); s.set_defaults(f=cmd_learn)
    s = sub.add_parser("stats"); s.set_defaults(f=cmd_stats)
    a = ap.parse_args(argv)
    a.f(a)
