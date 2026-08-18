$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$site = Resolve-Path (Join-Path $root "revenue-os\websites\main")
$docs = Join-Path $root "docs"

New-Item -ItemType Directory -Force -Path $docs | Out-Null

Get-ChildItem -LiteralPath $docs -Force | Remove-Item -Recurse -Force
Copy-Item -Path (Join-Path $site "*") -Destination $docs -Recurse -Force

$nojekyll = Join-Path $docs ".nojekyll"
if (-not (Test-Path -LiteralPath $nojekyll)) {
    New-Item -ItemType File -Path $nojekyll | Out-Null
}

Write-Host "Synced GitHub Pages site to $docs"

