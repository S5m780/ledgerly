---
name: 3d-designer
description: Turn a plain-language request for a physical object into a printable, checked parametric 3D design. Runs a plan → build → inspect → fix loop with four specialised agents (planner, builder, inspector, learner), exports STL/3MF/OBJ/GLB/SVG/PNG, and records lessons so the next design is faster. Use for any "design me a ...", "make a 3D model of ...", "I need a printable bracket/enclosure/gear/turntable ..." request.
---

# 3D designer

You are orchestrating a small design team. Never skip a phase; the value of this skill is that every
design gets planned before it is modelled and inspected before it is delivered.

## Setup (once per machine)
```bash
bash scripts/setup.sh        # installs openscad + python deps, checks xvfb for renders
```

## The loop

```
   prompt ──► PLAN ──► BUILD ──► INSPECT ──┬─ pass ─► EXPORT ─► LEARN ─► deliver
                        ▲                  │
                        └──── fix (≤3) ◄───┘ fail
```

1. **Scaffold.** `python -m designer new projects/<slug> --name "<title>"`. Write the user's request
   into `projects/<slug>/spec.md`: goal, testable **Requirements** bullets, non-goals, print bed, and a
   `tags:` line (mechanism words: gear, hinge, enclosure, motor, bearing, snap-fit …). Tags drive lesson retrieval.
2. **PLAN** — delegate to the `design-planner` agent with the spec path. It returns `plan.json`: hardware
   with critical dimensions, mechanism math, part list with print orientation, ordered steps with
   `done_when`, and `checks` (assertions over `CHECK` values the model must echo). Review it; resolve
   `open_questions` you can answer from the request, leave the rest as stated assumptions.
3. **BUILD** — delegate to `design-builder` with the plan. It writes the `.scad` (using `lib/`), echoes
   `CHECK key=value` lines for every number the plan wants verified, and runs `python -m designer build`.
4. **INSPECT** — delegate to `design-inspector`. It runs `python -m designer inspect`, renders views, and
   returns a findings list (severity, part, cause, fix). If anything fails, hand the findings back to the
   builder. At most 3 fix rounds; after that report what is still failing and why.
5. **EXPORT** — `python -m designer export projects/<slug> --fmt stl 3mf obj glb svg png` (or the
   formats the user asked for; see docs/EXPORT_FORMATS.md).
6. **LEARN** — delegate to `design-learner`. It records metrics, writes 1–3 lessons with tags, reinforces
   the lessons that were applied, and tunes defaults. This is what makes the next run faster.
7. **Deliver**: renders, the export folder, the BOM / wiring / assembly notes the builder wrote, and a
   short list of stated assumptions (measure-before-print items).

## Rules of thumb
- Every dimension is a named parameter at the top of the model; hardware envelopes live in `lib/hardware.scad`.
- Print without supports by default: re-orient in the part selector rather than telling the user to add supports.
- Anything load-bearing goes through a bearing race or a screw, never a printed rubbing face.
- Off-the-shelf parts whose dimensions the design depends on are listed as "measure before printing".
- Keep phases small and fast: compile only the parts you changed (`--part`), full run before delivery.

## Manual invocation
```bash
python -m designer run projects/<slug>       # whole loop, exits 1 on failure
python -m designer stats                     # what the learner knows so far
```
