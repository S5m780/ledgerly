# Assembly guide — Whatnot card-display turntable

Numbers refer to `BOM.md`. Read `build/inspection.md` for the final dimensions of your build.

## 0. Before printing: measure your motor
The base height is set by the motor. Measure the JGY-370 you actually received and set these in
`turntable.scad` (or in `lib/hardware.scad`) if they differ, then rebuild:

| Parameter | Default | What it is |
|---|---|---|
| `jgy_gb_h` | 26 | gearbox height along the output shaft |
| `jgy_gb_w` / `jgy_gb_len` | 32 / 37 | gearbox footprint |
| `jgy_shaft_from_end` | 16 | shaft axis distance from the gearbox end face |
| `jgy_shaft_len` | 14 | shaft length; if > lid height the lid gets an automatic relief hole |
| `jgy_body_d` / `jgy_body_len` | 24.4 / 32 | motor can |

Rebuild with `python -m designer run projects/whatnot-turntable` and the checks will tell you if it still fits.

## 1. Drive train
1. Press a **608 bearing (H2)** into the pocket on top of the centre tube in the base. It is a light press fit; use a 22 mm socket or the flat of a hex key set to push it square.
2. Slide the **rod (H3)** into the bearing until it bottoms (about 1 mm of relief is left under the bearing so the inner race floats).
3. Fit the **gear (P6)** hub-down over the rod: the hub sits 0.5 mm above the bearing. Nip the **grub screw (F4)** so the gear turns with the rod.
4. Push the **pinion (P7)** onto the motor's D-shaft, flat to flat, until it sits 1.5 mm above the gearbox face.
5. Drop the **motor (H1)** into the cradle: gearbox between the four corner ribs, can in the saddle, shaft up. The pinion should mesh with the gear with a little backlash and turn freely by hand. Fit the **strap (P8)** over the can with two **M3 × 8 (F2)**.
6. Wire everything as in `wiring.md`, stick the controller into its bay, fit the switch, pot and jack.

## 2. Lid
1. Press the second **608 bearing** into the pocket in the top of the lid (open side up). The 1 mm ledge underneath supports the outer race.
2. Lower the lid over the rod (the bearing boss enters the recess in the gear) and fix it with six **M3 × 8 (F1)**. Spin the gear by hand: no rubbing.
3. Drop the **spacer (P5)** over the rod so it rests on the bearing inner race. This is the only surface the plate weight rests on.

## 3. Plate
1. Screw the **hub (P4)** to the underside pocket of the plate with three **M3 × 6 countersunk (F3)**: the hex boss pokes through the plate.
2. Set the plate on the rod, hub disc down onto the spacer, and tighten the hex boss **grub screw** onto the rod. That is it: the plate is removable by loosening one grub screw (or, with a filed flat on the rod, by simply lifting).
3. Stick four **rubber feet (H10)** into the recesses under the base.

## 4. First run
- Switch **off**, knob to minimum, plug in 12 V.
- Switch **on**, raise the knob until it turns. Direction wrong? Swap the motor wires.
- Mark the knob position for your favourite 3 RPM (about 20 s per turn) with a dot.
- Drop the **card easel (P9)** into the shallow round recess in the middle of the plate; it self-centres so the card turns on the axis. The single slot takes a sleeved card (or a toploader), sunk 20 mm and leaning 12° back toward the camera; the low front lip has a finger notch.

## Two-piece plate (printers under 210 mm)
Set `plate_sections = 2`, print `plate` and `plate_half_b`. Push four 3 mm filament or steel pins into the holes along the straight edge, CA-glue the edge, clamp flat on a table for 10 minutes. The hub disc spans the seam and stiffens it.

## Printed-spindle alternative (no steel rod)
If you cannot get an 8 mm rod, print `gear` with `rod_d = 8` and glue an 8 mm printed pin (print vertically at 100 % infill, sand to fit the bearings). It is stiff enough for cards, less so for anything heavier.
