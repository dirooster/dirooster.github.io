$ErrorActionPreference = "Stop"

function Read-DotEnv($Path) {
    $values = @{}
    if (-not (Test-Path -LiteralPath $Path)) {
        return $values
    }
    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            return
        }
        $parts = $line.Split("=", 2)
        $values[$parts[0].Trim()] = $parts[1].Trim().Trim('"').Trim("'")
    }
    return $values
}

function Read-AuthFlag($Path, $Key) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }
    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if ($trimmed.StartsWith("${Key}:")) {
            return ($trimmed.Split(":", 2)[1].Trim().ToLowerInvariant() -eq "true")
        }
    }
    return $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envPath = Join-Path $root ".env"
$authPath = Join-Path $root "revenue-os\config\authorization.yaml"
$syncScript = Join-Path $root "revenue-os\tools\sync_github_pages.ps1"

if (-not (Read-AuthFlag $authPath "git_commit")) {
    throw "Refusing to commit/push: revenue-os/config/authorization.yaml has git_commit: false"
}

$envValues = Read-DotEnv $envPath
$username = $envValues["GITHUB_USERNAME"]
$repo = $envValues["GITHUB_REPO"]
$token = $envValues["GITHUB_TOKEN"]
$authorName = $envValues["GIT_AUTHOR_NAME"]
$authorEmail = $envValues["GIT_AUTHOR_EMAIL"]

if (-not $username) { $username = "dirooster" }
if (-not $repo) { $repo = "dirooster.github.io" }
if (-not $authorName) { $authorName = "Dmitrii Petukhov" }
if (-not $authorEmail) { $authorEmail = "tech.it.rooster@yandex.ru" }

if (-not $token -or $token -eq "replace_with_github_token") {
    throw "Set GITHUB_TOKEN in .env or use the browser/Git Credential Manager push flow."
}

& powershell -ExecutionPolicy Bypass -File $syncScript

Set-Location $root

if (-not (Test-Path -LiteralPath (Join-Path $root ".git"))) {
    git init | Out-Host
}

git branch -M main | Out-Host
git config user.name $authorName
git config user.email $authorEmail

$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$repoUrl = "https://api.github.com/repos/$username/$repo"
$exists = $false
try {
    Invoke-RestMethod -Uri $repoUrl -Headers $headers -Method Get | Out-Null
    $exists = $true
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -ne 404) {
        throw
    }
}

if (-not $exists) {
    $body = @{
        name = $repo
        private = $false
        auto_init = $false
        description = "AI systems architecture and revenue validation landing page"
    } | ConvertTo-Json
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json" | Out-Null
    Write-Host "Created GitHub repository $username/$repo"
}
else {
    Write-Host "GitHub repository $username/$repo already exists"
}

$remoteUrl = "https://github.com/$username/$repo.git"
$remoteExists = git remote | Where-Object { $_ -eq "origin" }
if ($remoteExists) {
    git remote set-url origin $remoteUrl
}
else {
    git remote add origin $remoteUrl
}

git add . | Out-Host

$status = git status --porcelain
if ($status) {
    git commit -m "Bootstrap revenue OS landing and outreach assets" | Out-Host
}
else {
    Write-Host "No local changes to commit"
}

git -c "http.https://github.com/.extraheader=AUTHORIZATION: bearer $token" push -u origin main | Out-Host

Write-Host "Pushed site to https://github.com/$username/$repo"
Write-Host "Enable GitHub Pages from branch main and folder /docs if it is not enabled automatically."

