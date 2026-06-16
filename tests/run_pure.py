"""
run_pure.py — bpy-free geometry test for bevel_bezier_corners.

Stubs bpy into sys.modules so the add-on's top-level imports succeed,
then execs the module and extracts rounded_corner for direct assertion.
Run with plain Python (no Blender required).
"""

import sys, types, math, os

# Stub bpy so the add-on's top-level bpy import and class definitions work
# without a real Blender runtime.
stub = types.ModuleType('bpy')
stub.types = types.SimpleNamespace(Operator=object, Panel=object)
props = types.ModuleType('bpy.props')
props.FloatProperty = lambda **k: None
stub.props = props
stub.utils = types.SimpleNamespace(register_class=lambda c: None, unregister_class=lambda c: None)
sys.modules['bpy'] = stub
sys.modules['bpy.props'] = props

ns = {}
addon = os.path.join(os.path.dirname(__file__), '..', 'addons', 'bevel_bezier_corners.py')
exec(open(addon, encoding='utf-8').read(), ns)
rounded_corner = ns['rounded_corner']

# 90-degree corner: prev=(-1,-1,0), corner=(1,-1,0), nxt=(1,1,0), radius=0.4
# Expected tangent points: t1=(0.6,-1.0,0.0), t2=(1.0,-0.6,0.0)
r = rounded_corner((-1, -1, 0), (1, -1, 0), (1, 1, 0), 0.4)

if r is None:
    print("FAIL: rounded_corner returned None for a 90-degree corner")
    sys.exit(1)

got_t1 = tuple(round(c, 3) for c in r.t1)
got_t2 = tuple(round(c, 3) for c in r.t2)
expected_t1 = (0.6, -1.0, 0.0)
expected_t2 = (1.0, -0.6, 0.0)

if got_t1 != expected_t1:
    print(f"FAIL: t1 expected {expected_t1}, got {got_t1}")
    sys.exit(1)

if got_t2 != expected_t2:
    print(f"FAIL: t2 expected {expected_t2}, got {got_t2}")
    sys.exit(1)

print("PURE_PASS")
sys.exit(0)
