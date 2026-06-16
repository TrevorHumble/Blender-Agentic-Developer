# Issue #0025 — Add-on: phyllotaxis (golden-angle) point generator

**Type:** ready. **Category:** Blender add-on (generative geometry).
**Depends on:** #0007 (Blender skills).
**Blocks:** none.
**Touches:** `addons/phyllotaxis.py` (new), `addons/README.md`.

## User story
As a Blender artist making generative or procedural art, I need a one-click generator that places N
points in the natural sunflower-seed (golden-angle) phyllotaxis pattern, so that I can build organic
radial arrangements — seed heads, scales, dot patterns — without hand-placing anything or wiring up
geometry nodes.

## Background
Phyllotaxis is the arrangement nature uses for sunflower seeds, pinecones, and succulents: point `i`
sits at angle `i × the golden angle (≈137.50776°)` and radius `scale × sqrt(i)`. The `sqrt` keeps the
points evenly dense; the golden angle (`360° × (2 − φ)`, φ the golden ratio) maximally avoids alignment,
giving the iconic interleaved spirals. The add-on creates a new mesh object whose vertices are the
phyllotaxis points (optionally lifted into a dome by a height falloff), so it works with the existing
test/eval harness (a bpy-free geometry function plus a bpy operator).

Geometry (`phyllotaxis_points(count, scale, dome=0.0)`):
- golden angle `ga = math.radians(360.0 * (2.0 - (1.0 + math.sqrt(5.0)) / 2.0))`.
- for `i` in `0..count-1`: `theta = i * ga`; `r = scale * math.sqrt(i)`;
  `x = r*cos(theta)`, `y = r*sin(theta)`, `z = dome * (1 - (r / (scale*sqrt(count-1)))**2)` if dome else 0.

## Acceptance criteria
Criteria 1-5 are literal/structural checks on the produced file; criterion 6 is a runtime check the
orchestrator verifies live and records.

1. **Given** the new file `addons/phyllotaxis.py`, **When** a reader greps it, **Then** it contains the
   literals `bl_info`, `def register(`, and `def unregister(`.
2. **Given** the file, **When** a reader greps it, **Then** it contains an Operator whose `bl_idname`
   literal is `mesh.add_phyllotaxis`, a `count` property declared with `IntProperty` (with a `min=`), and
   a `scale` property declared with `FloatProperty`.
3. **Given** the file, **When** a reader greps it, **Then** it contains a pure-geometry function named
   `phyllotaxis_points` that takes the count/scale and returns a list of (x, y, z) points, and that
   function body does not reference `bpy` (the bpy-free split the harness needs).
4. **Given** the file, **When** a reader greps it, **Then** the golden-angle constant is computed from the
   golden ratio (contains the literal `math.sqrt(5` and the literal `phyllotaxis`), not a hard-coded
   137.5 magic number alone.
5. **Given** the file, **When** a reader greps it, **Then** it registers the operator into the Add > Mesh
   menu (contains the literal `VIEW3D_MT_mesh_add`) and provides `register`/`unregister` that append/remove
   the menu entry.
6. **Given** the running Blender scene, **When** the operator runs with `count = 300` and `scale = 0.1`,
   **Then** a new mesh object is created with exactly 300 vertices, and the angle between consecutive
   points (about the origin) is the golden angle within a small tolerance. (Orchestrator verifies live,
   captures a viewport screenshot, and records the result.)

## Implementation plan
1. Create `addons/phyllotaxis.py`: `bl_info`; the pure `phyllotaxis_points(count, scale, dome=0.0)`
   function (AC3, bpy-free, golden angle from `math.sqrt(5)`); an operator `mesh.add_phyllotaxis` with
   `count` `IntProperty(min=1, default=300)`, `scale` `FloatProperty(default=0.1)`, and an optional
   `dome` `FloatProperty`; build a mesh from the points (verts only, or tiny faces) and link a new object.
2. Register the operator and append it to `bpy.types.VIEW3D_MT_mesh_add` (Add > Mesh menu); `unregister`
   removes the entry and unregisters the class.
3. Update `addons/README.md` to list the phyllotaxis add-on alongside the bevel add-on.
4. Verify live (AC6): run with count 300 / scale 0.1, confirm 300 verts and golden-angle spacing,
   screenshot.

## Out of scope
- Instancing real objects on the points (this version makes a vertex mesh; instancing is a follow-up).
- 3D phyllotaxis on a sphere (only the flat disk + optional dome falloff here).
- An eval-suite case for phyllotaxis (a follow-up that extends the eval harness to a second add-on).
