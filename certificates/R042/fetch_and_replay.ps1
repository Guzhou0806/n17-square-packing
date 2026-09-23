param(
  [Parameter(Mandatory=$true)][string]$OutputDir,
  [ValidateSet('records','containment','python','bigint')][string]$Mode='records',
  [int]$Jobs=4
)
$ErrorActionPreference='Stop'
$Verifier=Join-Path $PSScriptRoot 'verify.py'
if ($Mode -eq 'records') {
  python -X utf8 -B -S $Verifier --output $OutputDir
} elseif ($Mode -eq 'containment') {
  python -X utf8 -B -S $Verifier --containment --output $OutputDir
} elseif ($Mode -eq 'python') {
  python -X utf8 -B $Verifier --python-full --jobs $Jobs --output $OutputDir
} else {
  python -X utf8 -B -S $Verifier --bigint-full --jobs $Jobs --output $OutputDir
}
