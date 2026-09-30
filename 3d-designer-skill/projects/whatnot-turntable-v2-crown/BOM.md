# Bill of materials — turntable v2 (crown drive)

## Printed (PETG unless noted; see PRINT_H2S.md)
| Part | Qty | Notes |
|---|---|---|
| base | 1 | includes the axle post — print at 3 walls, 20 % infill, **post region is solid because it is under 8 mm wide** |
| lid | 1 | prints top-face-down (STL already flipped) |
| crown (42T) | 1 | 4 walls, 40 % infill; teeth up |
| pinion (12T) | 1 | 100 % infill, 5 walls; print 2 |
| hub | 1 | flange down; 4 walls, 50 % |
| spacer | 1 | 100 %; print 2 |
| plate Ø210 | 1 | PETG or PLA, 15 % gyroid, 3 walls; textured PEI gives a nice top finish if you flip it |
| motor_strap | 1 | flat |
| card_easel | 1+ | optional |

## Hardware
| Item | Qty | Spec | ~Price |
|---|---|---|---|
| N20 gearmotor | 1 | **GA12-N20 12 V, 20 RPM**, 3 mm D-shaft (15 RPM → 1.7–4.3 RPM at the plate; 30 RPM → 3.4–8.6) | $4 |
| 608ZZ bearing | 2 | 8 × 22 × 7 | $1 |
| PWM speed controller | 1 | 12 V, ≥ 1 A, **≤ 16 mm tall components**, pot on a lead or wire a panel pot | $3–5 |
| Panel potentiometer + knob | 1 | B10K (or the value your board uses), 6 mm shaft, M7 bushing | $2 |
| KCD1 rocker switch | 1 | SPST 15 × 21 mm, mounted sideways | $1 |
| DC-022B barrel jack | 1 | 5.5 × 2.1 mm, 12 mm hole | $1 |
| 12 V 1 A adapter | 1 | centre positive | $6 |
| M3 × 8 pan head screws | 8 | 6 lid + 2 strap (thread-forming into printed bosses) | |
| M3 × 6 countersunk | 3 | plate → hub flange | |
| Rubber feet Ø12 | 4 | adhesive | $2 |
| 22 AWG wire, PTFE or silicone grease | | | |
| Optional: 8 mm × 25 mm steel rod | 1 | only with `axle = "steel"` | $2 |

**≈ $20–25 in parts**, about 300 g of filament, no glue, no soldering except the two motor leads.
