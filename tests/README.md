# Tests

Dependency-free headless test harness for the Blender add-ons. No pytest, no pip install required. In-license: runs inside the free Blender 5.x Linux build used by CI.

## Scripts

| Script | Runtime | What it does |
|---|---|---|
| `run_pure.py` | Plain Python (no Blender) | Stubs `bpy` so the add-on's module-level imports succeed, then asserts pure geometry logic |
| `run_headless.py` | `blender --background --python` | Registers the add-on, exercises the operator, asserts output structure |
| `run_tests.ps1` | PowerShell | Orchestrates both; exits 1 if either sub-process exits non-zero |

## Running

```powershell
# Run both gates (PowerShell)
tests/run_tests.ps1

# Override Blender path
$env:BLENDER_EXE = "C:\path\to\blender.exe"; tests/run_tests.ps1
```

```
# Run headless gate directly
blender --background --python tests/run_headless.py
```

## License

All tests are in-license: no external service, no non-Anthropic key, no hosted account required. Blender is free and open-source.
