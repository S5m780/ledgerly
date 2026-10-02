# Inspection report — PASS

| part | watertight | volume mm³ | extents mm | overhang | issues |
|---|---|---|---|---|---|
| base.stl | yes | 90012 | [165.0, 165.0, 23.8] | 1% | — |
| lid.stl | yes | 62262 | [165.0, 165.0, 5.0] | 0% | — |
| crown.stl | yes | 10524 | [52.0, 52.0, 11.8] | 4% | — |
| pinion.stl | yes | 791 | [13.99, 13.99, 10.0] | 7% | — |
| hub.stl | yes | 12594 | [50.0, 50.0, 17.15] | 0% | — |
| spacer.stl | yes | 128 | [10.0, 10.0, 5.4] | 0% | — |
| plate.stl | yes | 234248 | [210.0, 210.0, 8.5] | 3% | — |
| motor_strap.stl | yes | 545 | [8.0, 30.6, 2.4] | 0% | — |
| card_easel.stl | yes | 37406 | [96.0, 96.0, 27.0] | 1% | — |

## Design checks

- ✅ `interference has no interference (volume 0.09 mm³)` 
- ✅ `base_height < 30` 
- ✅ `total_height < 40` 
- ✅ `ratio >= 3 and ratio <= 4` 
- ✅ `motor_far_radius < inner_r - 1` 
- ✅ `pcb_far_radius < inner_r - 0.5` 
- ✅ `bearing_span >= 10` 
- ✅ `hub_wall >= 2.5` 
- ✅ `crown_hub_d > hex_corner` 
- ✅ `pcb_top < panel_zc * 2` 
- ✅ `plate_d <= 320` 
- ✅ `total_height < 41` 

## Values echoed by the model

- base_height = 26.15
- total_height = 35.65
- plate_d = 210.0
- base_d = 165.0
- ratio = 3.5
- crown_R = 21.0
- motor_axis_z = 15.15
- pinion_top = 22.15
- motor_far_radius = 62.0
- inner_r = 80.1
- pcb_far_radius = 77.8091
- crown_rim_gap = 2.0
- bearing_span = 12.4
- post_top = 23.8
- hex_corner = 27.2509
- crown_hub_d = 28.0
- hub_wall = 3.14359
- panel_zc = 11.775
- panel_room = 18.75
- pcb_top = 21.0

## Compiler warnings

- interference: WARNING: Object may not be a valid 2-manifold and may need repair!
- interference: EXPORT-WARNING: Exported object may not be a valid 2-manifold and may need repair
