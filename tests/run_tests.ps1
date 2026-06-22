# run_tests.ps1 — test runner for bevel_bezier_corners.
# Runs the bpy-free pure test with plain Python, then the headless operator
# test under Blender background mode. Exits 1 if either process fails.

$blender = if ($env:BLENDER_EXE) { $env:BLENDER_EXE } else { 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' }
$root = (Resolve-Path "$PSScriptRoot\..")

if (-not (Test-Path $blender)) {
    Write-Host "TESTS_FAILED: blender not found at $blender"
    exit 1
}

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) {
    Write-Host "TESTS_FAILED: python not found"
    exit 1
}

Write-Host "=== Pure geometry test ==="
try {
    & $python "$root\tests\run_pure.py"
    $purecode = $LASTEXITCODE
} catch {
    Write-Host "TESTS_FAILED: run_pure.py threw: $_"
    $purecode = 1
}

Write-Host "=== Pure phyllotaxis test ==="
try {
    & $python "$root\tests\run_phyllotaxis_pure.py"
    $phyllocode = $LASTEXITCODE
} catch {
    Write-Host "TESTS_FAILED: run_phyllotaxis_pure.py threw: $_"
    $phyllocode = 1
}

Write-Host "=== Mutation/tamper gate ==="
try {
    & $python "$root\tests\mutation_harness.py"
    $mutationcode = $LASTEXITCODE
} catch {
    Write-Host "TESTS_FAILED: mutation_harness.py threw: $_"
    $mutationcode = 1
}

Write-Host "=== Headless operator test ==="
# --python-exit-code 1: Blender background mode exits 0 even on an unhandled
# Python exception by default; this forces exit 1 if run_headless.py raises
# (e.g. the add-on fails to load or register), so a broken test cannot false-pass.
try {
    & $blender --background --python-exit-code 1 --python "$root\tests\run_headless.py"
    $headlesscode = $LASTEXITCODE
} catch {
    Write-Host "TESTS_FAILED: run_headless.py threw: $_"
    $headlesscode = 1
}

if ($purecode -ne 0 -or $phyllocode -ne 0 -or $mutationcode -ne 0 -or $headlesscode -ne 0) {
    Write-Host "TESTS_FAILED (run_pure.py=$purecode, run_phyllotaxis_pure.py=$phyllocode, mutation_harness.py=$mutationcode, run_headless.py=$headlesscode)"
    exit 1
}

Write-Host "ALL_TESTS_PASS"
exit 0
