param(
  [Parameter(Mandatory=$true)][string]$OutputDir,
  [string]$SourceDir = ".replay-sources/r038"
)
$ErrorActionPreference = "Stop"
$Commit = "ac464dd06ded72e2f6eb2c2f3d510b01391c056d"
$ExpectedSha = "5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3"
$Url = "https://raw.githubusercontent.com/Mira-acc/17squares/$Commit/certificates/lower_bound_4p614153/certificate.json"
$SourcePath = Join-Path $SourceDir "certificate.json"
if (Test-Path $OutputDir) { throw "Output directory already exists / 输出目录已经存在: $OutputDir" }
New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
Write-Host "Downloading the pinned upstream certificate / 正在下载锁定的上游证书"
Invoke-WebRequest -Uri $Url -OutFile $SourcePath
$ActualSha = (Get-FileHash -Algorithm SHA256 $SourcePath).Hash.ToLowerInvariant()
if ($ActualSha -ne $ExpectedSha) { throw "Certificate SHA mismatch / 证书 SHA 不匹配: $ActualSha" }
Write-Host "Pinned SHA verified / 锁定 SHA 已验证: $ActualSha"
python -X utf8 -B -S certificates/R038/verify.py --certificate $SourcePath --output $OutputDir
if ($LASTEXITCODE -ne 0) { throw "R038 replay failed / R038 复验失败" }
Write-Host "R038 replay completed / R038 复验完成"
