# Fast Landing Deployment

The current website is static:

`revenue-os/websites/main`

## Recommended First Deployment

Use Cloudflare Pages or GitHub Pages for a fast preview. No backend is required.

To create a direct-upload archive:

```powershell
powershell -ExecutionPolicy Bypass -File revenue-os\tools\package_site.ps1
```

Archive output:

`revenue-os/deploy/dist/rooster-tech-landing.zip`

## GitHub Pages Path

1. Create a private or public GitHub repository.
2. Push this workspace.
3. In repository settings, enable Pages from the branch.
4. Use `/docs` as the Pages folder.

See `GITHUB_PAGES.md`.

## Cloudflare Pages Path

1. Create a Pages project.
2. Connect the Git repository or upload the `revenue-os/websites/main` folder directly.
3. Build command: empty.
4. Output directory: `revenue-os/websites/main` when using the repo; `/` when uploading the folder directly.

## Production Gate

Production deployment remains blocked until `config/authorization.yaml` has:

```yaml
deploy_production: true
```
