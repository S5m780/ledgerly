# Lessons (append-only, machine copy in lessons.json)

- **L001** (enclosure, general, plate) — Build round plates and rims as one rotate_extrude() profile; a union of coincident cylinders leaves a 4-face seam edge and a non-watertight STL. _(from whatnot-turntable)_
- **L002** (bearing, general, hub) — A part with features on both faces (boss below, hub above) cannot print flat: split the smaller feature into its own part (e.g. a spacer ring) instead of adding supports. _(from whatnot-turntable)_
- **L003** (clamp, motor, strap) — Arched clamps/straps print on their side as a 2-D profile; standing them up makes the crown a 90 deg overhang. _(from whatnot-turntable)_
- **L004** (enclosure, gear, general, pocket) — Pocket ceilings printed face-down are flat overhangs the area metric under-reports: give pockets 45 deg conical walls and keep any remaining bridge under ~30 mm. _(from whatnot-turntable)_
- **L005** (bearing, gear, turntable) — Sink the lid bearing boss into a recess in the drive gear: it saves ~4 mm of base height versus stacking bearing above gear. _(from whatnot-turntable)_
- **L006** (enclosure, motor, turntable) — Orient a gearmotor tangentially (can along the base's circumference) so the base diameter is set by the plate gear, not by motor length. _(from whatnot-turntable)_
- **L007** (enclosure, general, lid) — Run an interference view (intersection() of every assembled pair, must be empty) before shipping: a lid locating lip crossing the screw bosses is invisible in renders but shows as ~120 mm3 overlap. _(from whatnot-turntable)_
