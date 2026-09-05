param(
    [Parameter(Mandatory = $true)][string]$UpstreamRoot,
    [Parameter(Mandatory = $true)][string]$WorkRoot1,
    [Parameter(Mandatory = $true)][string]$WorkRoot2,
    [Parameter(Mandatory = $true)][string]$PrivateRoot1,
    [Parameter(Mandatory = $true)][string]$PrivateRoot2,
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$receiptPath = Join-Path $root 'builds\TEX_MUTEX_RECEIPT.json'
$mutexName = 'Global\InterlanguageTeXSlotV1'
$waitSeconds = 600
$texMutex = [System.Threading.Mutex]::new($false, $mutexName)
$held = $false
$failure = $null

$receipt = [ordered]@{
    schema = 'stacks-r41-tex-mutex-execution/v1'
    candidate_id = 'stacks-errata-a04446e-r41'
    mutex_name = $mutexName
    wait_timeout_seconds = $waitSeconds
    acquisition_started_at_utc = [DateTime]::UtcNow.ToString('o')
    acquired = $false
    acquired_at_utc = $null
    abandoned_mutex_recovered = $false
    holder_pid = $PID
    guarded_commands = @()
    released = $false
    released_at_utc = $null
    passed = $false
    failure = $null
}

function Save-Receipt {
    $parent = Split-Path -Parent $receiptPath
    [IO.Directory]::CreateDirectory($parent) | Out-Null
    $json = ($receipt | ConvertTo-Json -Depth 12) + "`n"
    [IO.File]::WriteAllText($receiptPath, $json, [Text.UTF8Encoding]::new($false))
}

function Invoke-GuardedPython {
    param([string]$Role, [string[]]$Arguments)
    & $Python @Arguments
    $code = $LASTEXITCODE
    $receipt.guarded_commands += [ordered]@{ role = $Role; exit_code = $code }
    Save-Receipt
    if ($code -ne 0) {
        throw "$Role failed with exit code $code"
    }
}

foreach ($path in @($WorkRoot1, $WorkRoot2, $PrivateRoot1, $PrivateRoot2)) {
    if (Test-Path -LiteralPath $path) {
        throw "Build and private roots must all be new and absent: $path"
    }
}
if (-not (Test-Path -LiteralPath $UpstreamRoot -PathType Container)) {
    throw "Pinned upstream root is missing: $UpstreamRoot"
}
Save-Receipt

try {
    try {
        $held = $texMutex.WaitOne([TimeSpan]::FromSeconds($waitSeconds))
    }
    catch [System.Threading.AbandonedMutexException] {
        $held = $true
        $receipt.abandoned_mutex_recovered = $true
    }
    if (-not $held) {
        throw "Timed out after $waitSeconds seconds acquiring $mutexName; no TeX command was started."
    }
    $receipt.acquired = $true
    $receipt.acquired_at_utc = [DateTime]::UtcNow.ToString('o')
    Save-Receipt

    Invoke-GuardedPython 'fresh_candidate_authority_build_1' @(
        (Join-Path $root 'replay-build.py'), '--upstream-root', $UpstreamRoot,
        '--work-root', $WorkRoot1, '--private-evidence-root', $PrivateRoot1
    )
    Invoke-GuardedPython 'fresh_candidate_authority_build_2' @(
        (Join-Path $root 'replay-build.py'), '--upstream-root', $UpstreamRoot,
        '--work-root', $WorkRoot2, '--private-evidence-root', $PrivateRoot2
    )
    Invoke-GuardedPython 'deterministic_pdf_comparison' @(
        (Join-Path $root 'deterministic-replay.py'), '--first-private-build-root', $PrivateRoot1
    )
    Invoke-GuardedPython 'immediate_log_and_build_preflight' @(
        (Join-Path $root 'build-receipt.py'), '--preflight'
    )
}
catch {
    $failure = $_
    $receipt.failure = $_.Exception.Message
}
finally {
    if ($held) {
        $texMutex.ReleaseMutex()
        $receipt.released = $true
        $receipt.released_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    $texMutex.Dispose()
    $receipt.passed = ($null -eq $failure -and $receipt.acquired -and $receipt.released)
    Save-Receipt
}

if ($null -ne $failure) {
    throw $failure
}

& $Python (Join-Path $root 'build-receipt.py')
if ($LASTEXITCODE -ne 0) {
    throw "Final post-release build receipt binding failed with exit code $LASTEXITCODE"
}

Write-Output (([ordered]@{
    passed = $true
    mutex = $mutexName
    abandoned_mutex_recovered = $receipt.abandoned_mutex_recovered
    receipt = $receiptPath
} | ConvertTo-Json -Compress))
