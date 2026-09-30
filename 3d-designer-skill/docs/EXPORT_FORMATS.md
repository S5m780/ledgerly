# Export formats

`python -m designer export <project> --fmt <formats...>` (defaults to `plan.json["exports"]`).

| Format | Produced by | Use it for |
|---|---|---|
| `stl` | OpenSCAD | slicers (Cura, PrusaSlicer, Bambu Studio), the universal default |
| `3mf` | trimesh | slicers; smaller and carries units/colour; preferred by Bambu/Prusa |
| `obj`, `ply` | trimesh | Blender, viewers, mesh tools |
| `glb` / `gltf` | trimesh | web viewers, AR quick-look, Three.js |
| `off`, `amf`, `csg` | OpenSCAD | CGAL / legacy / debugging the CSG tree |
| `svg`, `dxf` | trimesh silhouette (top-down projection of the STL) | laser-cut templates, 2-D drawings, drilling guides |
| `png` | OpenSCAD (headless via xvfb) | previews for the inspector and for the user; views listed in `plan.json["views"]` |

## STEP / parametric B-rep
OpenSCAD is mesh-only. If a STEP file is needed (CNC shops, Fusion/SolidWorks users), the model has to be
re-expressed in CadQuery or Build123d. The pipeline is format-agnostic: point `plan.json["model"]` at a
`.py` file and add a `cadquery` branch in `builder.run_openscad`'s caller. Not wired by default to keep
the dependency footprint small.

## Custom views
```json
"views": [{"name": "assembly", "part": "assembly", "camera": "0,0,25,55,0,35,520"}]
```
`camera` is OpenSCAD's `--camera=tx,ty,tz,rotx,roty,rotz,dist`.
