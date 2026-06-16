# review-gate.ps1 — Claude Code Stop hook
# Blocks a turn from ending unless the Ralph loop has reached a legitimate exit.
# Legitimate exits: a reviewer writes PASS, or the severity adjudicator writes
# EXIT_AUTHORIZED to .review_state\verdict.txt because all remaining defects are
# inconsequential (see #0020 and DESIGN.md).

$ErrorActionPreference = 'SilentlyContinue'

try {
    $raw = [Console]::In.ReadToEnd()
    $in  = $raw | ConvertFrom-Json
} catch {
    # Unparseable stdin — do not block; let the turn end.
    exit 0
}

# Empty or unparseable stdin returns $null in PowerShell 5.1 without throwing.
if ($null -eq $in) { exit 0 }

# CHECK 1: stop_hook_active
# The documented infinite-loop guard: if this hook itself triggered a Stop event,
# honour it immediately rather than recursing.
if ($in.stop_hook_active -eq $true) {
    exit 0
}

# CHECK 2: MAX_ITERS
# Iteration counter backstop — guarantees termination even if the model never
# writes a verdict artifact.
$MAX_ITERS   = 25
if (-not $in.cwd -and -not $env:CLAUDE_PROJECT_DIR) { exit 0 }
$base        = if ($in.cwd) { $in.cwd } else { $env:CLAUDE_PROJECT_DIR }
$stateDir    = Join-Path $base '.review_state'
$counterFile = Join-Path $stateDir 'iter_count.txt'
$statusFile  = Join-Path $stateDir 'status.txt'

if (-not (Test-Path $stateDir)) {
    try { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null } catch {}
}

$count = 0
if (Test-Path $counterFile) {
    try {
        $count = [int](Get-Content $counterFile -Raw).Trim()
    } catch {
        # Counter file exists but is non-numeric — fail toward the cap so a
        # corrupted file cannot suppress termination indefinitely.
        $count = $MAX_ITERS
    }
}

$count++

try {
    Set-Content -Path $counterFile -Value $count -Encoding ascii -ErrorAction Stop
} catch {
    try { Set-Content -Path $statusFile -Value 'CAP_HIT' -Encoding ascii -ErrorAction Stop } catch {}
    exit 0
}

if ($count -gt $MAX_ITERS) {
    try { Set-Content -Path $statusFile -Value 'CAP_HIT' -Encoding ascii } catch {}
    try { Set-Content -Path $counterFile -Value '0' -Encoding ascii } catch {}
    exit 0
}

# CHECK 3: verdict
# Read the verdict artifact written by the orchestrator loop.
# PASS comes from a reviewer; EXIT_AUTHORIZED comes from the severity adjudicator.
$verdictFile = Join-Path $stateDir 'verdict.txt'
$verdict     = ''
try {
    $verdict = (Get-Content $verdictFile -Raw).Trim()
} catch {
    $verdict = ''
}

if ($verdict -eq 'PASS' -or $verdict -eq 'EXIT_AUTHORIZED') {
    try { Set-Content -Path $counterFile -Value '0' -Encoding ascii } catch {}
    try { [IO.File]::WriteAllText($verdictFile, '') } catch {}
    exit 0
}

# CHECK 4: block
# No legitimate exit found — re-inject the task.
# Output shape: {"decision":"block","reason":"<imperative>"}
# reason: write PASS (reviewer) or EXIT_AUTHORIZED (severity adjudicator) to the
# verdict path before stopping.
$blockObj = @{
    decision = 'block'
    reason   = "The Ralph loop has not reached a legitimate exit. To exit: a reviewer must return PASS, or the severity adjudicator must write EXIT_AUTHORIZED to '$verdictFile' because all remaining defects are inconsequential. Continue the review loop now."
}
$blockObj | ConvertTo-Json -Compress
exit 0
