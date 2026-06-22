"""
mutation_harness.py — tamper gate for the bpy-free pure tests.

Deliberately breaks a known behavior in an add-on (a "mutant"), points the
matching pure test at the mutated copy, and asserts the test FAILS. A mutant
the test still passes is a SURVIVED mutant — a real hole where the gate is
blind to that break. A mutant whose pattern can't be applied is BROKEN — it
proves nothing. Exit 0 only if every mutant was caught and none was broken.

Pure Python, no Blender. Run from the repo root: python tests/mutation_harness.py
"""

import os
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
_ADDONS = os.path.join(_ROOT, 'addons')

BEVEL = os.path.join(_ADDONS, 'bevel_bezier_corners.py')
PHYLLO = os.path.join(_ADDONS, 'phyllotaxis.py')
RUN_PURE = os.path.join(_HERE, 'run_pure.py')
RUN_PHYLLO = os.path.join(_HERE, 'run_phyllotaxis_pure.py')

# (name, test_script, addon_path, env_var, old_substring, new_substring, pass_sentinel)
# Each old->new breaks a real behavior the named test must catch.
# pass_sentinel is the success line the test prints when it PASSES; its presence
# means the break went undetected (survived), regardless of return code.
MUTANTS = [
    ("bevel-chamfer", RUN_PURE, BEVEL, 'BEVEL_ADDON_PATH',
     'h = (4.0/3.0) * math.tan(alpha / 4.0) * r_eff',
     'h = 0.0', 'PURE_PASS'),
    ("bevel-wrong-arc-constant", RUN_PURE, BEVEL, 'BEVEL_ADDON_PATH',
     '(4.0/3.0) * math.tan(alpha / 4.0)',
     '(1.0) * math.tan(alpha / 4.0)', 'PURE_PASS'),
    ("bevel-wrong-setback", RUN_PURE, BEVEL, 'BEVEL_ADDON_PATH',
     'd = radius / math.tan(theta / 2.0)',
     'd = radius * math.tan(theta / 2.0)', 'PURE_PASS'),
    ("phyllotaxis-golden-angle-hardcode", RUN_PHYLLO, PHYLLO, 'PHYLLO_ADDON_PATH',
     'ga = math.radians(360.0 * (2.0 - (1.0 + math.sqrt(5.0)) / 2.0))',
     'ga = math.radians(137.5)', 'PHYLLOTAXIS_PURE_PASS'),
    ("phyllotaxis-radius-linear", RUN_PHYLLO, PHYLLO, 'PHYLLO_ADDON_PATH',
     'r = scale * math.sqrt(i)',
     'r = scale * i', 'PHYLLOTAXIS_PURE_PASS'),
    ("phyllotaxis-dome-sign", RUN_PHYLLO, PHYLLO, 'PHYLLO_ADDON_PATH',
     'dome * (1.0 - (r / r_max) ** 2)',
     'dome * (1.0 + (r / r_max) ** 2)', 'PHYLLOTAXIS_PURE_PASS'),
]


def _apply_mutant(name, test_script, addon_path, env_var, old, new, sentinel):
    """Run one mutant. Return 'caught', 'survived', 'errored', or 'broken'.

    A catch is credited ONLY when the test's own assertion fired: non-zero exit,
    success sentinel absent, and a FAIL line present. A non-zero exit with no
    FAIL line (crash, traceback, import error, bad path) is 'errored' — the test
    failed for the WRONG reason and proves nothing.
    """
    src = open(addon_path, encoding='utf-8').read()
    n = src.count(old)
    if n != 1:
        print(f"MUTANT_BROKEN: {name} (pattern matched {n} times)")
        return 'broken'

    mutated = src.replace(old, new)
    fd, path = tempfile.mkstemp(suffix='.py', prefix='mutant_')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(mutated)
        env = dict(os.environ)
        env[env_var] = path
        proc = subprocess.run([sys.executable, test_script], env=env,
                              capture_output=True, text=True)
        out = proc.stdout or ''
        passed = sentinel in out
        has_fail = any(line.startswith('FAIL') for line in out.splitlines())
        if proc.returncode == 0 or passed:
            return 'survived'
        if has_fail:
            return 'caught'
        tail = ((proc.stderr or '') + out).strip()[:300]
        print(f"ERRORED: {name} (test failed without an assertion — wrong reason)")
        print(tail)
        return 'errored'
    finally:
        os.remove(path)


def main():
    if not MUTANTS:
        print("HARNESS_ERROR: no mutants defined")
        sys.exit(1)

    caught = 0
    failed = 0
    total = len(MUTANTS)
    for mutant in MUTANTS:
        name = mutant[0]
        result = _apply_mutant(*mutant)
        if result == 'caught':
            caught += 1
            print(f"caught: {name}")
        elif result == 'survived':
            failed += 1
            print(f"SURVIVED: {name}")
        else:
            # 'errored' and 'broken' both count as failures.
            failed += 1

    print(f"guards caught {caught}/{total}")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
