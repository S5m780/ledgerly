# Printing on the Bambu Lab H2S

Files: `build/plates/plate_1.3mf` and `plate_2.3mf` (all parts, already laid out for the 350 × 320 bed),
or the individual STLs in `build/export/`.  Open the 3MF in Bambu Studio → *Import geometry only* if asked
→ it lands on the bed with every object positioned. Check the build volume in your printer profile
(H2S: 350 × 320 × 325 mm) before slicing.

| Setting | Value | Why |
|---|---|---|
| Filament | PETG (Bambu PETG HF or Basic) | gears and bearing pockets like PETG's toughness; PLA is fine for the plate and easel |
| Process | 0.20 mm Standard | crown & pinion at **0.12 mm Fine** if you want quieter teeth |
| Walls | 3 (base, lid, plate), 4 (crown, hub), 5 (pinion) | set per object in the object list |
| Infill | 20 % gyroid; pinion & spacer 100 % | |
| Supports | **off** | every part is oriented flat; nothing overhangs > 45° |
| Bridging | "Detect bridging perimeters" on | the crown has a 22 mm bridged ceiling over its bearing pocket |
| Bed | textured PEI, 70 °C | no brim needed for PETG on textured PEI; add a 3 mm brim for the plate if your sheet is worn |
| Cooling | PETG defaults; min layer time 8 s for the pinion | small part |
| Seam | rear | keeps the seam off the visible rim of the plate |

Print order that lets you start assembling early: plate 2 (base + lid) first while you print the
drive parts on plate 1.

Fit tuning: bearing pockets are modelled at 22.15 mm; if a 608 goes in loose, set `fit_tight = 0.05`
and reprint the crown/hub. The post is 7.85 mm: if a bearing will not slide on, a wrap of 400-grit
sandpaper on the post fixes it in a minute; if it is loose, set `post_d = 7.95`.
