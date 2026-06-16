# addons/

Blender 5.1 add-ons produced by the blender-orchestrator pipeline.

---

## bevel_bezier_corners.py

Rounds sharp corners of any active POLY or BEZIER curve into circular-arc
bezier fillets. Each corner becomes two bezier knots with explicit `FREE`
handles; straight segments between fillets are preserved.

### Install

**Option A — Blender Preferences (persistent)**

1. Blender menu: Edit > Preferences > Add-ons > Install.
2. Navigate to `addons/bevel_bezier_corners.py` and confirm.
3. Enable the add-on in the list.

**Option B — Text Editor (session only)**

1. Open the Blender Text Editor, open `bevel_bezier_corners.py`.
2. Run Script (Alt+P or the Run Script button).

### Use

1. Select a curve object in the viewport.
2. Open the Sidebar (N key) > Edit tab > Bevel Corners panel.
3. Click **Bevel Bezier Corners**. Adjust **Radius** to taste.

The operator is also available via the F3 search menu as "Bevel Bezier Corners".

### Radius parameter

Sets the fillet radius in scene units. The setback distance is automatically
clamped so fillets on adjacent corners never overlap. Corners that are nearly
straight (colinear within 1e-4 rad) are left unchanged.

### Geometry function

`rounded_corner()` is bpy-free (uses only the `math` standard library) and
is unit-tested outside Blender. See `issues/0018-bevel-bezier-corners-addon.md`
for the fillet geometry derivation.
