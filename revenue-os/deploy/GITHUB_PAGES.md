# GitHub Pages Deployment

Status: local site is prepared for GitHub Pages via the repository `/docs` folder.

GitHub profile:

- Username: `dirooster`
- Profile: https://github.com/dirooster

Recommended repository:

- `dirooster.github.io`

This gives the clean URL:

`https://dirooster.github.io/`

## Local Sync

Run after changing the source website:

```powershell
powershell -ExecutionPolicy Bypass -File revenue-os\tools\sync_github_pages.ps1
```

This copies:

`revenue-os/websites/main`

to:

`docs`

and adds `.nojekyll`.

## GitHub Setup

1. Create a GitHub repository named `dirooster.github.io`.
2. Push this workspace.
3. Open repository settings.
4. Go to Pages.
5. Source: Deploy from a branch.
6. Branch: `main`.
7. Folder: `/docs`.

## Push Commands

Run only after `git_commit: true` is approved:

```powershell
git init
git branch -M main
git add .gitignore docs revenue-os README.md main.py "AUTONOMOUS REVENUE AGENT — MASTER EXECUTION SPEC.md"
git commit -m "Bootstrap revenue OS landing and outreach assets"
git remote add origin https://github.com/dirooster/dirooster.github.io.git
git push -u origin main
```

## Automated Push With Local Token

Do not paste the token into chat. Put it in local `.env`:

```env
GITHUB_USERNAME=dirooster
GITHUB_REPO=dirooster.github.io
GITHUB_TOKEN=...
GIT_AUTHOR_NAME=Dmitrii Petukhov
GIT_AUTHOR_EMAIL=tech.it.rooster@yandex.ru
```

Then run:

```powershell
powershell -ExecutionPolicy Bypass -File revenue-os\tools\publish_github_pages.ps1
```

## Needed From Owner To Push Automatically

- Confirmation that `git_commit: true` is allowed.
- Repository `dirooster.github.io` created on GitHub.
- Either authenticated Git credential manager in the browser flow or a remote URL configured manually.
