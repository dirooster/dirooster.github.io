# Contact Form Options

Current site status:

- GitHub Pages static site.
- Contact form exists on the page.
- If `data-form-endpoint` is empty, the form opens a prepared `mailto:` message.
- SMTP password is never exposed in browser JavaScript.

## Recommended Options

### Option A - Formspree

Fastest static-site option.

1. Create a Formspree form.
2. Set destination email to `tech.it.rooster@yandex.ru`.
3. Copy the endpoint URL.
4. Put it into the form:

```html
data-form-endpoint="https://formspree.io/f/..."
```

Official docs:

- https://formspree.io/
- https://developers.cloudflare.com/pages/tutorials/add-an-html-form-with-formspree/

### Option B - EmailJS

Good if you want client-side template sending without your own backend. EmailJS keeps email service credentials server-side, while the browser uses public identifiers.

Official docs:

- https://www.emailjs.com/
- https://www.emailjs.com/docs/sdk/options/

### Option C - Cloudflare Worker

Best technical option if you want full control. Store SMTP/API credentials as Worker secrets, not in GitHub Pages.

Official docs:

- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.cloudflare.com/workers/configuration/environment-variables/

## Recommendation

Use Formspree first. It is the fastest path to a working static landing form. Move to Cloudflare Worker only if form volume, customization, or deliverability requires it.

