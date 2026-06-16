"""
run_headless.py — bpy operator test for bevel_bezier_corners.

Run under: blender --background --python tests/run_headless.py

Builds a cyclic POLY square, runs the bevel operator, then asserts the
result is a cyclic BEZIER spline with 8 bezier points.
"""

import sys
import os
import runpy

import bpy

ADDON_PATH = os.path.join(os.path.dirname(__file__), '..', 'addons', 'bevel_bezier_corners.py')

# Load and register the add-on into the running Blender session.
addon_globals = runpy.run_path(ADDON_PATH)
addon_globals['register']()

# Build a new curve object — don't rely on the default scene.
curve_data = bpy.data.curves.new(name='TestSquare', type='CURVE')
curve_data.dimensions = '3D'

spline = curve_data.splines.new('POLY')
spline.use_cyclic_u = True
# POLY spline starts with 1 point; add 3 more for a 4-corner square.
spline.points.add(3)
corners = [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)]
for i, (x, y, z) in enumerate(corners):
    # POLY point.co is (x,y,z,w).
    spline.points[i].co = (x, y, z, 1.0)

obj = bpy.data.objects.new('TestSquare', curve_data)
bpy.context.collection.objects.link(obj)

# Select and activate the object so the operator's poll passes.
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Run the operator.
result = bpy.ops.curve.bevel_bezier_corners(radius=0.4)

if 'FINISHED' not in result:
    print(f"FAIL: operator returned {result}, expected FINISHED")
    sys.exit(1)

# Verify the result spline.
splines = list(curve_data.splines)
if len(splines) != 1:
    print(f"FAIL: expected 1 spline after operator, got {len(splines)}")
    sys.exit(1)

sp = splines[0]

if sp.type != 'BEZIER':
    print(f"FAIL: spline type expected BEZIER, got {sp.type}")
    sys.exit(1)

if not sp.use_cyclic_u:
    print("FAIL: spline is not cyclic")
    sys.exit(1)

n_pts = len(sp.bezier_points)
if n_pts != 8:
    print(f"FAIL: expected 8 bezier points, got {n_pts}")
    sys.exit(1)

print("HEADLESS_PASS")
sys.exit(0)
