# Khyber Spice Invader — website

A fully static site (plain HTML/CSS/JS, no build tools, no npm) rebuilding
khyberspice.co.nz with a design of its own. It's deployable to Netlify
with **zero build configuration**.

## What's in here

- `index.html`, `products.html`, `about.html`, `shipping.html`, `contact.html`, `404.html` — the pages
- `data/products.json` — the entire product catalog + category list. **This is the file to edit to add products.**
- `css/styles.css` — the whole design system
- `js/main.js` — nav, basket drawer, basket persistence (localStorage)
- `build.py` — regenerates the HTML pages from shared header/footer partials. Only needed if you're editing page structure/copy, not for adding products.

## 1. Push to GitHub

```bash
cd khyber-site
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 2. Deploy on Netlify

1. netlify.com → **Add new site → Import an existing project**
2. Choose GitHub, authorize, pick this repo
3. Build settings: leave build command **blank** (or `true`), publish directory `.` — `netlify.toml` already sets this
4. **Deploy site**

Every future push to `main` redeploys automatically.

## 3. Growing the product catalog

The current catalog (86 products across all 11 real aisles) was compiled by
hand from the live khyberspice.co.nz listings — the full store has 1,000+
SKUs across 58 listing pages, which wasn't practical to transcribe product-by-
product in one sitting. To fill it out, either:

**Option A — Shopify export (fastest, if you get admin access later).**
Shopify Admin → Products → Export → all products → CSV. Send me that file
and I'll convert it straight into `data/products.json` in one pass, images
included.

**Option B — Paste more listing pages to me.**
I can keep pulling category pages from the live site in batches and append
them to `data/products.json` — just ask me to continue with a given category.

**Option C — Edit `data/products.json` directly.**
Each product is:
```json
{ "name": "Product Name", "category": "spices", "price": 4.99, "unit": "100g", "stock": "in" }
```
`category` must match a `slug` in the `categories` array at the top of the
file. `stock` is `"in"` or `"out"`. `note` is optional (shows as a small
badge, e.g. `"On special"`). No rebuild needed — the shop page reads this
file directly at runtime.

## 4. Turning on real sign-in (Netlify Identity)

The "Sign in" button and Account page are wired to **Netlify Identity** —
a real, free authentication system built into Netlify, no custom backend
needed. To activate it:

1. Netlify dashboard → your site → **Site configuration → Identity → Enable Identity**
2. That's it — "Sign in" will now open a real signup/login form, and
   signed-in users see their name/email on the Account page.
3. Order tracking on that page is intentionally a placeholder until
   Stripe checkout exists (see below) — there's no order to track yet.

## 5. How product photos work

Rather than manually attaching an image to all 86 products, each product
card guesses the photo URL from the original store's predictable naming
pattern (`PRODUCT_NAME_medium.jpg`) and silently falls back to a category
icon if that guess doesn't resolve. Real photos will show for products
whose name matches the CDN file exactly; the rest show a clean icon
instead of a broken image. As you get proper product photography, replace
this with real `image` URLs per product in `data/products.json`.

## 6. The Khyber Bot

`js/bot.js` is a lightweight rule-based FAQ assistant (hours, delivery,
locations, stock, etc.) — it runs entirely in the browser, no API key or
backend required. Anything it doesn't recognise offers an "Email the
store" button that opens a pre-filled email to sales@khyberspice.co.nz.
To upgrade it to a real AI model later, replace `answerQuery()` with a
call to a serverless function that talks to an LLM API (never call an AI
API directly from browser JS — that would expose your API key).

## 7. Adding Stripe later

The basket (`js/main.js`) already tracks items and totals in `localStorage`
and renders a disabled "Checkout — coming soon" button. To wire up Stripe:

1. Add a Netlify Function (`netlify/functions/create-checkout.js`) that
   creates a Stripe Checkout Session server-side (never put your Stripe
   secret key in front-end JS)
2. Replace the disabled checkout button's `onclick` to POST the cart to
   that function and redirect to the returned Stripe session URL
3. Add your Stripe keys as Netlify environment variables (Site settings →
   Environment variables) — never commit them to the repo

Happy to build this out with you when you're ready — just ask.

## Notes

- Contact form currently shows a placeholder alert on submit. To make it
  actually send email, wire it to Netlify Forms (add `data-netlify="true"`
  to the `<form>`) or a Netlify Function.
- Google Maps embeds on the About page use the same map IDs as the current
  site.
- All copy and prices were sourced from the live site in August 2026 —
  double check prices before launch in case anything's changed since.
