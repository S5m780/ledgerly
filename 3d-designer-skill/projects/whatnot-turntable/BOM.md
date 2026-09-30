# Bill of materials — Whatnot card-display turntable

Prices are typical hobby-supplier prices (Amazon / AliExpress / eBay, 2026) and are only a guide.

## Printed parts (PETG recommended; PLA is fine for the plate and easel)

| # | Part | Qty | Print notes |
|---|------|-----|-------------|
| P1 | `base` | 1 | 0.2 mm layers, 3 perimeters, 20 % infill, no supports. ~5 h |
| P2 | `lid` | 1 | prints top-face-down (the STL is already flipped). ~2.5 h |
| P3 | `plate` | 1 | 210 mm — needs a 220 mm bed. Use `plate` + `plate_half_b` with `plate_sections=2` for small printers. 15 % infill |
| P4 | `hub` | 1 | 50 % infill, 4 perimeters |
| P5 | `spacer` | 1 | 100 % infill. Tiny; print 2 in case one is lost |
| P6 | `gear` (51T) | 1 | 4 perimeters, 30 % infill. Bridges a 30 mm recess: enable "detect bridging perimeters" |
| P7 | `pinion` (17T) | 1 | 5 perimeters, 60 % infill. The D-bore is a push fit on the motor shaft |
| P8 | `motor_strap` | 1 | prints on its side (STL is already oriented) |
| P9 | `card_easel` | 1 | centred single-slot stand for a sleeved card, 12° back-lean, drops into the plate recess |

## Electro-mechanical parts

| # | Item | Qty | Spec / search terms | ~Price |
|---|------|-----|---------------------|--------|
| H1 | Worm-gear motor | 1 | **JGY-370 12 V DC, 15 RPM**, 6 mm D-shaft. (10 RPM version gives 1.3–3.3 RPM at the plate; 20 RPM gives 2.7–6.7) | $9–14 |
| H2 | Bearing 608ZZ | 2 | 8 × 22 × 7 mm skate bearing | $1 |
| H3 | Steel rod Ø8 × 40 mm | 1 | "8 mm linear shaft" or an M8 bolt shank cut to 40 mm, ends deburred. Optional: file a small flat for the grub screws | $2 |
| H4 | PWM DC motor speed controller | 1 | 12 V-capable, ≥ 2 A, **with the potentiometer on a lead / panel mount** (e.g. "1803BK" style or "6–28 V 3 A PWM controller with external pot"). Board must fit 60 × 45 × 18 mm | $3–6 |
| H5 | Panel potentiometer | 1 | Only if H4's pot is board-mounted: B10K (check board), 6 mm shaft, M7 bushing, plus a knob | $2 |
| H6 | Rocker switch KCD1 | 1 | SPST, 15 × 21 mm body, 13 × 19 mm cutout, 6 A 250 V | $1 |
| H7 | DC barrel jack, panel mount | 1 | DC-022B 5.5 × 2.1 mm, 12 mm mounting hole | $1 |
| H8 | 12 V power adapter | 1 | 12 V 1 A (or larger) with 5.5 × 2.1 mm plug, centre positive | $6 |
| H9 | Wire | ~1 m | 22 AWG stranded, red + black | — |
| H10 | Adhesive rubber feet | 4 | Ø12 mm, fit the recesses under the base | $2 |

## Fasteners

| # | Item | Qty | Where |
|---|------|-----|-------|
| F1 | M3 × 8 self-tapping / thread-forming screw (pan head) | 6 | lid → base bosses |
| F2 | M3 × 8 pan head | 2 | motor strap → cradle bosses |
| F3 | M3 × 6 countersunk | 3 | plate → hub disc |
| F4 | M3 × 5 grub screw (cup point) | 2 | gear hub → rod, hex hub → rod |
| F5 | M3 heat-set inserts (optional) | 5 | gear hub, hex hub, hub disc: use if you want repeatable disassembly |
| — | Fast-set CA glue (only for a two-piece plate) | | |

## Tools
3D printer, 2 mm hex key, small Phillips screwdriver, wire stripper, soldering iron (only if H4 needs its pot moved), file (rod deburring).

**Total (excluding filament and printer time): about $30–40.**
