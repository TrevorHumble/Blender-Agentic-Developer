# Issue #0018 — Add-on: bevel/round bezier corners

**Type:** ready. **Category:** Blender add-on (the first real add-on; product, not orchestrator system).
**Depends on:** #0007 (Blender skills).
**Blocks:** #0017 (committing this — the first add-on with `bpy` code — is #0017's graduation trigger).
**Touches:** `addons/bevel_bezier_corners.py` (new), `addons/README.md` (new).

## User story
As a Blender artist with a curve that has sharp corners, I need a one-click way to round those corners
into true bezier fillets of a radius I choose, so that I get smooth rounded corners that Blender's
existing tools do not produce on a curve.

## Background
Blender has no built-in operator that rounds the corners of an existing curve into bezier fillets.
The test object in the live scene is `Plane`, a cyclic `POLY` curve forming an axis-aligned 2×2 square
(corners at (±1, ±1, 0), side length 2). The feature replaces each sharp corner with a circular-arc fillet expressed
as two bezier knots with handles, leaving straight segments between the fillets.

Geometry (for each corner vertex `V` with previous neighbor `A` and next neighbor `B`):
- `a = (A - V).normalized()`, `b = (B - V).normalized()`; interior angle `theta = acos(clamp(a·b,-1,1))`.
- Near-colinear corners (`theta` near 0 or near pi) are left unfilleted.
- Setback `d = radius / tan(theta/2)`, clamped to half of each adjacent edge so neighbouring fillets do
  not overlap; effective radius `r_eff = d * tan(theta/2)`.
- Tangent points `T1 = V + a*d`, `T2 = V + b*d` become two bezier knots.
- Arc sweep `alpha = pi - theta`; handle length `h = (4/3) * tan(alpha/4) * r_eff`. The arc-side handle at
  `T1` points toward `V` (`T1 - a*h`) and at `T2` toward `V` (`T2 - b*h`); the straight-side handles lie
  along the edges so inter-corner segments stay straight. This cubic matches a circular arc closely.

## Acceptance criteria
Criteria 1-6 are literal/structural checks on the produced file. Criterion 7 is a runtime check the
orchestrator verifies live in Blender and records.

1. **Given** the new file `addons/bevel_bezier_corners.py`, **When** a reader greps it, **Then** it
   contains the literal strings `bl_info`, `def register(`, and `def unregister(`.
2. **Given** the file, **When** a reader greps it, **Then** it contains an Operator whose
   `bl_idname` literal is `curve.bevel_bezier_corners` and a `bl_label`, and a `radius` property
   declared with `FloatProperty` (the radius is `> 0` via a `min=`).
3. **Given** the file, **When** a reader greps it, **Then** it contains a Panel class with
   `bl_space_type = 'VIEW_3D'`, `bl_region_type = 'UI'`, and a `poll` that restricts it to curve objects
   (contains the literal `'CURVE'`).
4. **Given** the file, **When** a reader greps it, **Then** it contains `def rounded_corner(`, and the
   body of that function (between its `def` and the next top-level `def`) contains no occurrence of the
   literal `bpy` — the bpy-free geometry split that #0017 needs.
5. **Given** the file, **When** a reader greps it, **Then** it contains the literal `use_cyclic_u` (the
   operator preserves the input spline's cyclic flag) and the literal `colinear` (the named guard that
   leaves near-colinear corners unfilleted).
6. **Given** the file, **When** a reader greps it, **Then** it contains the four-thirds arc factor
   written as one of the literals `4/3`, `4.0/3.0`, or `4.0 / 3.0`, and sets handles explicitly (contains
   the literals `handle_left`, `handle_right`, and the `'FREE'` handle type), so the fillet is a real
   circular arc, not Blender AUTO.
7. **Given** the running Blender scene with the `Plane` cyclic square curve, **When** the operator runs
   with a radius of `0.4`, **Then** the curve becomes a cyclic `BEZIER` spline with 8 bezier points
   (two per original corner) and none of the four original sharp 90° corners remain. (Orchestrator
   verifies live, captures a viewport screenshot, and records the result.)

## Implementation plan
1. Create `addons/bevel_bezier_corners.py`: `bl_info`, the pure `rounded_corner` geometry function
   (AC4, bpy-free), the operator `curve.bevel_bezier_corners` with a `radius` `FloatProperty(min=...)`,
   a `VIEW_3D`/`UI` panel gated to curves, and `register`/`unregister`.
2. The operator reads the active curve, and for each spline (POLY or BEZIER) builds a replacement BEZIER
   spline: per corner, call `rounded_corner` to get `T1`/`T2` and their handles; emit straight handles
   between corners; preserve `use_cyclic_u`; skip near-colinear corners. Write the new splines back.
   A BEZIER input spline's existing handles are discarded — only its knot positions are used as the
   polyline vertices. `rounded_corner` returns the two tangent points and their handle vectors.
3. Verify the geometry live: confirm the API (`splines.new('BEZIER')`, `bezier_points.add`,
   `handle_left`/`handle_right`, `handle_*_type='FREE'`) against the Blender RAG before relying on it.
4. Write `addons/README.md`: what the add-on does, how to install/run it, and the radius parameter.

## Out of scope
- A modifier or non-destructive (geometry-nodes) version; this edits the curve data directly.
- Per-corner radius control or corner selection; one radius applies to all corners this version.
- Packaging as a 4.2+ extension (`blender_manifest.toml`); a single-file `bl_info` add-on is enough here.
