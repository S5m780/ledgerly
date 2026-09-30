# Inspection report — PASS

| part | watertight | volume mm³ | extents mm | overhang | issues |
|---|---|---|---|---|---|
| base.stl | yes | 134808 | [180.0, 180.0, 39.4] | 1% | — |
| lid.stl | yes | 78354 | [180.0, 180.0, 9.0] | 0% | — |
| gear.stl | yes | 32496 | [79.45, 79.49, 16.0] | 5% | — |
| pinion.stl | yes | 3666 | [28.32, 28.44, 8.0] | 0% | — |
| hub.stl | yes | 9311 | [50.0, 50.0, 13.0] | 0% | — |
| spacer.stl | yes | 183 | [12.0, 12.0, 3.0] | 0% | — |
| plate.stl | yes | 232858 | [210.0, 210.0, 8.5] | 2% | — |
| plate_half_b.stl | yes | 115894 | [104.85, 209.99, 8.5] | 2% | — |
| motor_strap.stl | yes | 985 | [43.2, 14.9, 8.0] | 3% | — |
| card_easel.stl | yes | 35888 | [96.0, 96.0, 27.0] | 2% | — |

## Design checks

- ✅ `interference has no interference (volume 0.00 mm³)` 
- ✅ `abs(center_distance - 51) < 0.01` 
- ✅ `ratio >= 2.5 and ratio <= 4` 
- ✅ `motor_far_radius < inner_r - 1` 
- ✅ `pcb_far_radius < inner_r - 0.5` 
- ✅ `base_height < 50` 
- ✅ `total_height < 60` 
- ✅ `plate_d <= 220` 
- ✅ `rod_span_hi > hub_hex_top - 3` 

## Values echoed by the model

- base_height = 42.4
- total_height = 57.4
- plate_d = 210.0
- base_d = 180.0
- center_distance = 51.0
- gear_od = 79.5
- pinion_od = 28.5
- ratio = 3.0
- motor_shaft_tip = 42.4
- lid_z0 = 39.4
- relief = True
- rod_span_lo = 15.4
- rod_span_hi = 55.4
- hub_hex_top = 57.4
- motor_far_radius = 85.1072
- inner_r = 87.6
- ok = True
- pcb_far_radius = 84.2333

## Compiler warnings

- interference: WARNING: Object may not be a valid 2-manifold and may need repair!
- interference: EXPORT-WARNING: Exported object may not be a valid 2-manifold and may need repair
