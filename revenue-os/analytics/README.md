# Analytics

Current state:

- CTA clicks and lead-form submissions are stored locally in browser `localStorage`.
- No external analytics service is connected.

Recommended production option:

- Cloudflare Web Analytics if deploying with Cloudflare Pages.
- Plausible if a paid privacy-friendly analytics service is acceptable.
- Google Analytics only if broader ad/remarketing tooling becomes necessary.

Required before production analytics:

1. Chosen provider.
2. Domain or site ID.
3. Authorization to add the production tracking script.

