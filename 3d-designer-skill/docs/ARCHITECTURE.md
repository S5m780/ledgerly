# Architecture

## Why a loop, not a single prompt
A model written in one shot is usually wrong in ways that only show up in a slicer: a seam that is not
watertight, a pocket ceiling that needs support, a motor that does not fit. The loop makes those checks
mechanical (`designer inspect`) and makes the *fix* the builder's job, with the inspector as the gate.
The learner turns each fix into a rule the planner sees next time, so the same mistake is not made twice.

## Phases and contracts

| Phase | Input | Output | Exit criterion |
|---|---|---|---|
| plan | spec.md, knowledge | plan.json | every requirement maps to a part/step/check |
| build | plan.json | model.scad, build/*.stl, build/manifest.json | all parts compile, 0 warnings |
| inspect | manifest, plan.checks | build/inspection.{json,md}, renders | exit 0 |
| export | plan.exports | build/export/* | every requested file exists |
| learn | inspection, manifest, timings | knowledge/* | lessons recorded, weights updated |

### CHECK protocol
The model echoes `CHECK key=value key2=value2` lines. The builder parses them into a flat dict; the
inspector evaluates `plan.json["checks"]` (Python boolean expressions) against it. A model can also
echo `ok=false` to fail itself. This keeps geometric truth in the model and policy in the plan.

### Inspector metrics
- **watertight / winding**: trimesh; a non-watertight mesh is a failure.
- **bed fit**: sorted extents vs sorted bed dims.
- **overhang fraction**: area of faces whose normal points down steeper than 50°, excluding the bottom
  0.3 mm. > 15 % fails, > 3 % is noted. It misses ceilings of pockets (they face down but are flat);
  the inspector agent looks at the renders for those.
- **interference**: a part flagged `must_be_empty` (a view made of `intersection()`s of assembled parts) must compile to volume ≈ 0.
- **thin fragments**: connected components under `min_wall_mm` with volume < 50 mm³ (modelling slips).

## Adaptive learning
- `lessons.json` — `{id, lesson, tags[], weight, source}`; planner retrieves by tag overlap, ranked by
  overlap then weight. `lessons.md` is the human-readable mirror.
- **Reinforcement** — lessons applied to a plan get ×1.1 when the inspection passes, ×0.95 when it fails.
- `heuristics.json` — defaults (material, nozzle, layer, min wall) folded in from passing projects.
- `metrics.jsonl` — per run: phase seconds, parts, warnings, failures, iterations. `designer stats`
  shows the slowest phase and first-time pass rate, the two numbers to optimise.

## Extending
- New hardware → `lib/hardware.scad` as an envelope module with named dims and a `clearance` argument.
- New check → echo it from the model and add the expression to `plan.json["checks"]`.
- New format → `designer/exporter.py` (OpenSCAD-native or via trimesh). STEP: see EXPORT_FORMATS.md.
- New agent behaviour → edit `.claude/agents/*.md`; the skill in `.claude/skills/3d-designer/SKILL.md`
  is the orchestration order.
