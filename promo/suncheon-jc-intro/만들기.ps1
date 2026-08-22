# 순천승주청년회의소 인트로 영상 만들기
# 파워셸에서 이 파일을 우클릭 → "PowerShell에서 실행" 하거나
#   powershell -ExecutionPolicy Bypass -File .\만들기.ps1
# 로 실행하세요.

param(
  [string]$Source = "C:\Users\gilau\Videos\4K Video Downloader+\Landscapes Volume 4K (UHD).mp4",
  [string]$Out    = "",
  [switch]$PlanOnly,      # 어느 구간을 쓸지 목록만 보고 싶을 때
  [switch]$SubsOnly,      # 멘트만 고쳐서 다시 뽑을 때 (컷 재사용, 훨씬 빠름)
  [double]$AudioStart = -1
)

$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING  = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-Python {
  $cands = @(
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
  )
  foreach ($c in $cands) { if (Test-Path $c) { return $c } }
  foreach ($n in @("py","python","python3")) {
    $g = Get-Command $n -ErrorAction SilentlyContinue
    if ($g) { return $g.Source }
  }
  throw "파이썬을 찾을 수 없습니다. https://www.python.org 에서 설치한 뒤 다시 실행하세요."
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "ffmpeg 가 PATH 에 없습니다.  winget install Gyan.FFmpeg  로 설치한 뒤 창을 새로 여세요."
}
if (-not (Test-Path -LiteralPath $Source)) {
  throw "원본 영상을 찾을 수 없습니다: $Source"
}

$py = Find-Python
Write-Host "파이썬 : $py"
Write-Host "원본   : $Source"
Write-Host ""

$argv = @("$here\build_intro.py", "--source", $Source)
if ($Out)         { $argv += @("--out", $Out) }
if ($PlanOnly)    { $argv += "--plan-only" }
if ($SubsOnly)    { $argv += "--subs-only" }
if ($AudioStart -ge 0) { $argv += @("--audio-start", "$AudioStart") }

& $py @argv
if ($LASTEXITCODE -ne 0) { throw "빌드가 실패했습니다. 위 메시지를 확인하세요." }

if (-not $PlanOnly) {
  $final = if ($Out) { $Out } else { Join-Path (Split-Path -Parent $Source) "순천승주청년회의소_인트로.mp4" }
  if (Test-Path -LiteralPath $final) {
    Write-Host ""
    Write-Host "완성본을 폴더에서 엽니다."
    Start-Process explorer.exe "/select,`"$final`""
  }
}
