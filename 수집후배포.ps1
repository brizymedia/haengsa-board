# 수집 후 배포 — 한국 PC 에서 실행한다.
#
#   .\수집후배포.ps1
#
# 공공데이터포털이 해외 IP 를 차단해 GitHub Actions 에서는 수집이 안 된다.
# 이 스크립트가 로컬에서 수집해 events.json 을 커밋·푸시하면
# GitHub Actions 가 이어받아 사이트를 배포한다.
#
# 매일 자동으로 돌리려면 Windows 작업 스케줄러에 등록:
#   프로그램: powershell.exe
#   인수:    -NoProfile -ExecutionPolicy Bypass -File "C:\클로드코드2\수집후배포.ps1"

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$env:DATA_GO_KR_KEY = [Environment]::GetEnvironmentVariable("DATA_GO_KR_KEY", "User")
if (-not $env:DATA_GO_KR_KEY) {
    Write-Host "DATA_GO_KR_KEY 사용자 환경변수가 없습니다. setx 로 먼저 등록하세요."
    exit 1
}

Set-Location collector
python run.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "수집 실패 — 커밋하지 않습니다."
    exit 1
}

Set-Location ..
git add site/data/events.json
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "변경 없음 — 푸시할 것이 없습니다."
    exit 0
}
git commit -m "일일 수집 $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push
Write-Host "푸시 완료 — GitHub Actions 가 1~2분 안에 사이트를 갱신합니다."
