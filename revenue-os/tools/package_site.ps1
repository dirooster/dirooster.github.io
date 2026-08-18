$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$site = Resolve-Path (Join-Path $root "revenue-os\websites\main")
$dist = Join-Path $root "revenue-os\deploy\dist"
$zip = Join-Path $dist "rooster-tech-landing.zip"

New-Item -ItemType Directory -Force -Path $dist | Out-Null
if (Test-Path -LiteralPath $zip) {
    Remove-Item -LiteralPath $zip -Force
}

Compress-Archive -Path (Join-Path $site "*") -DestinationPath $zip -Force
Write-Host "Created $zip"

