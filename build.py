#!/usr/bin/env python3
"""Static site assembler for Khyber Spice Invader.
Run: python3 build.py
Writes fully-formed HTML files (no build step needed to deploy —
the OUTPUT of this script is what goes on Netlify)."""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

def head(title, desc, active, ambient=False):
    nav_items = [
        ("index.html", "Home"),
        ("products.html", "Shop"),
        ("about.html", "About"),
        ("shipping.html", "Shipping"),
        ("contact.html", "Contact"),
        ("account.html", "Account"),
    ]
    nav_html = "\n".join(
        f'<a href="{href}" class="{"active" if href==active else ""}"{" id=\"accountNavLink\"" if href=="account.html" else ""}>{label}</a>'
        for href, label in nav_items
    )
    ambient_html = """<div class="ambient">
  <div class="blob b1"></div>
  <div class="blob b2"></div>
  <div class="blob b3"></div>
  <span class="icon" style="top:12%; left:8%; font-size:46px; animation-delay:-2s;">&#127798;</span>
  <span class="icon" style="top:22%; right:12%; font-size:38px; animation-delay:-8s;">&#127806;</span>
  <span class="icon" style="top:55%; left:5%; font-size:34px; animation-delay:-4s;">&#129381;</span>
  <span class="icon" style="top:68%; right:8%; font-size:44px; animation-delay:-11s;">&#127861;</span>
  <span class="icon" style="top:85%; left:18%; font-size:30px; animation-delay:-6s;">&#127850;</span>
  <span class="icon" style="top:38%; right:30%; font-size:28px; animation-delay:-14s;">&#129347;</span>
</div>""" if ambient else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="css/styles.css">
<script>
  // Apply saved theme before paint to avoid a flash of the wrong theme.
  (function(){{ var t = localStorage.getItem('khyber_theme'); if (t && t !== 'khyber') document.documentElement.setAttribute('data-theme', t); }})();
</script>
</head>
<body>
<div class="grain"></div>
{ambient_html}

<div class="vip-strip">
  <div class="wrap">
    <span class="tag">VIP</span>
    <span>Ask in-store about our VIP Customer Card &mdash; start earning cashback rewards.</span>
  </div>
</div>

<div class="utility-bar">
  <div class="wrap">
    <span>822 Manukau Road, Royal Oak, Auckland <span class="dot">·</span> Open Mon&ndash;Sun 9:00am&ndash;8:30pm</span>
    <span><a href="tel:+6496251766">09 625 1766</a></span>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a href="index.html" class="brand">
      <img src="assets/logo-cropped.png" alt="Khyber Spice Invader" style="height:38px; width:auto; border-radius:6px; object-fit:contain; flex-shrink:0;">
      <div class="brand-text">
        <span class="name">Khyber Spice Invader</span>
        <span class="tag">Royal Oak · Est. 2005</span>
      </div>
    </a>
    <div class="header-search">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" id="headerSearchInput" placeholder="Search the shop...">
    </div>
    <nav class="main-nav" id="mainNav">
      {nav_html}
      <div class="mobile-nav-extra">
        <div class="header-search mobile-search">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="mobileSearchInput" placeholder="Search the shop...">
        </div>
        <p class="mobile-nav-label">Colour theme</p>
        <div class="theme-options">
          <button class="theme-option" data-theme="khyber"><span class="swatch-dot" style="background:#F0981F;"></span>Classic</button>
          <button class="theme-option" data-theme="light"><span class="swatch-dot" style="background:#D97F0A;"></span>Light</button>
          <button class="theme-option" data-theme="sunset"><span class="swatch-dot" style="background:#FF4D8D;"></span>Sunset</button>
          <button class="theme-option" data-theme="midnight"><span class="swatch-dot" style="background:#4DD4FF;"></span>Midnight</button>
        </div>
      </div>
    </nav>
    <div class="header-actions">
      <div class="theme-toggle-wrap">
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="Change colour theme">
          &#127912;
          <span class="theme-toggle-dot" id="themeDot"></span>
        </button>
        <div class="theme-teaser" id="themeTeaser">Tap to try a different look &mdash; 4 colour themes!</div>
        <div class="theme-popover" id="themePopover">
          <p>Colour theme</p>
          <div class="theme-options">
            <button class="theme-option" data-theme="khyber"><span class="swatch-dot" style="background:#F0981F;"></span>Classic</button>
            <button class="theme-option" data-theme="light"><span class="swatch-dot" style="background:#D97F0A;"></span>Light</button>
            <button class="theme-option" data-theme="sunset"><span class="swatch-dot" style="background:#FF4D8D;"></span>Sunset</button>
            <button class="theme-option" data-theme="midnight"><span class="swatch-dot" style="background:#4DD4FF;"></span>Midnight</button>
          </div>
        </div>
      </div>
      <button class="btn btn-header btn-small cart-toggle" id="cartToggle" type="button">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
        <span class="cart-label">Basket</span> <span class="cart-count" id="cartCount" style="display:none;">0</span>
      </button>
      <button class="nav-toggle" id="navToggle" type="button" aria-label="Toggle menu">&#9776;</button>
    </div>
  </div>
</header>
"""

FOOT = """
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-about">
        <div class="brand" style="margin-bottom:16px;">
          <img src="assets/logo-cropped.png" alt="Khyber Spice Invader" style="height:38px; width:auto; border-radius:6px; object-fit:contain; flex-shrink:0;">
          <div class="brand-text">
            <span class="name">Khyber Spice Invader</span>
            <span class="tag">Royal Oak · Est. 2005</span>
          </div>
        </div>
        <p>One stop shop for Indian, Sri Lankan, Pakistani, Iranian and Arabic food and spices. Variety is the spice of life.</p>
      </div>
      <div>
        <h5>Shop</h5>
        <ul>
          <li><a href="products.html">All products</a></li>
          <li><a href="products.html#spices">Spices</a></li>
          <li><a href="products.html#daals-lentils">Daals &amp; Lentils</a></li>
          <li><a href="products.html#rice-flour">Rice &amp; Flour</a></li>
        </ul>
      </div>
      <div>
        <h5>Info</h5>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="shipping.html">Shipping &amp; delivery</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h5>Get in touch</h5>
        <ul>
          <li><a href="tel:+6496251766">09 625 1766</a></li>
          <li><a href="tel:+6496241365">09 624 1365</a></li>
          <li><a href="mailto:sales@khyberspice.co.nz">sales@khyberspice.co.nz</a></li>
          <li><a href="https://www.facebook.com/people/Khyber-Spice-Invader-Royal-Oak/100056588722990/" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Khyber Spice Invader Royal Oak</span>
      <span><a href="terms.html">Terms</a> &middot; <a href="privacy.html">Privacy</a></span>
      <span>822 Manukau Road, Royal Oak, Auckland 1061</span>
    </div>
  </div>
</footer>

<div class="cart-overlay" id="cartOverlay"></div>
<aside class="cart-drawer" id="cartDrawer" aria-label="Shopping basket">
  <div class="cart-drawer-head">
    <h3>Your Basket</h3>
    <button class="cart-drawer-close" id="cartClose" type="button" aria-label="Close basket">&times;</button>
  </div>
  <div class="cart-items" id="cartItems"></div>
  <div class="cart-drawer-foot">
    <div class="cart-total" id="cartTotal"><span>Subtotal</span><strong>$0.00</strong></div>
    <button class="btn btn-primary" style="width:100%; justify-content:center;" disabled title="Online checkout is launching soon">
      Checkout — coming soon
    </button>
    <p class="cart-note">Online payment via Stripe is being set up. For now, call the store to place a phone order for anything in your basket.</p>
  </div>
</aside>

<div class="ff-overlay" id="ffOverlay">
  <div class="ff-modal" id="ffModal"></div>
</div>

<div class="product-modal-overlay" id="productModalOverlay">
  <div class="product-modal" id="productModal"></div>
</div>

<div class="bot-teaser" id="botTeaser">
  <button type="button" id="botTeaserClose" aria-label="Dismiss">&times;</button>
  &#128075; Need a hand? Ask me about stock, delivery, or even cooking tips.
</div>
<button class="bot-launcher" id="botLauncher" type="button" aria-label="Open Khyber Bot">
  <span class="bl-ring"></span>
  <span class="bl-icon">&#128172;</span>
  <span class="bl-label">Ask Khyber Bot</span>
</button>
<div class="bot-panel" id="botPanel">
  <div class="bot-head">
    <div>
      <h4>Khyber Bot</h4>
      <span>Usually replies instantly</span>
    </div>
    <button class="bot-close" id="botClose" type="button" aria-label="Close chat">&times;</button>
  </div>
  <div class="bot-messages" id="botMessages"></div>
  <div class="bot-suggestions">
    <button type="button">Store hours?</button>
    <button type="button">Best rice for yellow daal?</button>
    <button type="button">How long to cook rice?</button>
  </div>
  <div class="bot-input-row">
    <input type="text" id="botInput" placeholder="Ask a question...">
    <button id="botSend" type="button" aria-label="Send">&#8594;</button>
  </div>
</div>

<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
<script src="js/main.js"></script>
<script src="js/bot.js"></script>
<script src="js/auth.js"></script>
<script src="js/flavor-finder.js"></script>
<script src="js/transitions.js"></script>
</body>
</html>
"""

def write(path, html):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
home_body = """
<section class="hero">
  <video id="spiceVideo" autoplay muted loop playsinline aria-hidden="true">
    <source src="assets/spice-pour.webm" type="video/webm">
    <source src="assets/spice-pour.mp4" type="video/mp4">
  </video>
  <div class="wrap">
    <div class="hero-eyebrow">Indian &middot; Sri Lankan &middot; Pakistani &middot; Iranian &middot; Arabic Grocery &middot; Est. 2005</div>
    <h1>Variety is the<br><em>spice of life.</em></h1>
    <p class="lede">Khyber Spice Invader has stocked Royal Oak's kitchens since 2005 &mdash; whole and ground spices, daals, rice, ghee, snacks and Ayurvedic personal care, at prices that make the trip worth it.</p>
    <div class="hero-actions">
      <a href="products.html" class="btn btn-primary">Shop the range</a>
      <button class="btn btn-header-fill ff-trigger" id="ffTrigger" type="button">&#127798; Find Your Flavor</button>
    </div>
    <div class="hero-strip">
      <span>Mon&ndash;Sun, 9am&ndash;8:30pm</span>
      <span class="sep">&middot;</span>
      <span>822 Manukau Road, Royal Oak</span>
      <span class="sep">&middot;</span>
      <span>Delivery anywhere in NZ</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="section-eyebrow">Shop by aisle</div>
        <h2>Everything a subcontinental kitchen needs</h2>
      </div>
      <a href="products.html" class="btn btn-outline btn-small">View full shop &rarr;</a>
    </div>
    <div class="cat-grid" id="homeCatGrid"></div>
  </div>
</section>

<section class="section" style="border-bottom:none;">
  <div class="wrap story-grid">
    <div>
      <div class="section-eyebrow">Since 2005</div>
      <h2>Two decades of stocking the aisle no one else does</h2>
      <p>We started this business in 2005, delivering to the unique and traditional grocery needs of migrants from different countries living in New Zealand. We specialise in premium quality products across spices, lentils, rice, flour, packaged and frozen foods, cosmetics, and household goods &mdash; and we ship anywhere in the country.</p>
      <a href="about.html" class="btn btn-outline btn-small">Read our full story</a>
    </div>
    <div class="ticket">
      <div class="row"><span>Founded</span><span>2005</span></div>
      <div class="row"><span>Location</span><span>822 Manukau Rd, Royal Oak</span></div>
      <div class="row"><span>Hygiene grade</span><span>&ldquo;A&rdquo; &mdash; Auckland Council</span></div>
      <div class="row"><span>Delivery area</span><span>Nationwide, NZ</span></div>
      <div class="row"><span>On Facebook</span><span>508 followers &middot; 16 check-ins</span></div>
      <div class="row"><span>Payment</span><span>Card in-store &middot; online soon</span></div>
    </div>
  </div>
</section>

<section class="section" style="border-bottom:none; padding-top:0;">
  <div class="wrap">
    <div class="section-eyebrow">On our shelves right now</div>
    <h2 style="font-family:var(--font-display); font-size:clamp(22px,2.6vw,30px); font-weight:600; margin:0 0 20px;">Real brands, not filler</h2>
    <div class="brand-chip-row">
      <span>Kashish</span><span>Ayur</span><span>Daawat</span><span>India Gate</span>
      <span>Alokozay</span><span>Nirapara</span><span>Sahara</span><span>Qataghan</span>
      <span>Ace</span><span>Bajaj</span><span>Baidynth</span><span>Avon Agro</span>
    </div>
  </div>
</section>
"""

home_script = """
<script>
document.addEventListener('khyber:data-ready', () => {
  const grid = document.getElementById('homeCatGrid');
  grid.innerHTML = ALL.categories.map(c => {
    const count = ALL.products.filter(p=>p.category===c.slug).length;
    return `<a class="cat-tile accent-${c.accent}" href="products.html#${c.slug}">
      <span class="lid"></span>
      <h3>${c.label}</h3>
      <p>${c.blurb}</p>
      <span class="count">${count > 0 ? count + ' lines stocked' : 'Catalogue expanding'}</span>
    </a>`;
  }).join('');
});
</script>
"""

write("index.html", head("Khyber Spice Invader — Indian &amp; Subcontinental Grocery, Royal Oak", "One stop shop for Indian, Sri Lankan, Pakistani, Iranian and Arabic food and spices in Royal Oak, Auckland since 2005.", "index.html", ambient=True) + home_body + FOOT.replace("</body>", home_script + "</body>"))

# ------------------------------------------------------------------
# PRODUCTS / SHOP
# ------------------------------------------------------------------
shop_body = """
<section class="info-page">
  <div class="wrap">
    <h1>The Shop</h1>
    <p class="lede">Search or filter by aisle. Prices shown are for pickup from the Royal Oak store &mdash; online checkout is coming soon, call in the meantime to arrange delivery.</p>

    <div class="shop-layout">
      <aside class="shop-sidebar">
        <div class="search-box">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="searchInput" placeholder="Search products...">
        </div>
        <div class="filter-block">
          <h4>Aisles</h4>
          <div class="cat-filter-list" id="catFilterList"></div>
        </div>
        <div class="filter-block">
          <h4>Availability</h4>
          <div class="cat-filter-list">
            <button data-stock="all" class="active">All items</button>
            <button data-stock="in">In stock only</button>
          </div>
        </div>
      </aside>

      <div>
        <div class="results-meta" id="resultsMeta"></div>
        <div class="product-grid" id="productGrid"></div>
      </div>
    </div>
  </div>
</section>
"""

shop_script = """
<script>
let state = { cat: 'all', stock: 'all', q: '' };

const swatchColor = { turmeric: '#E7A31C', paprika: '#C1440E', cardamom: '#5B7553' };

function accentFor(slug){
  const c = ALL.categories.find(c=>c.slug===slug);
  return c ? swatchColor[c.accent] : '#E7A31C';
}
function labelFor(slug){
  const c = ALL.categories.find(c=>c.slug===slug);
  return c ? c.label : slug;
}

function renderFilters(){
  const list = document.getElementById('catFilterList');
  const counts = {};
  ALL.products.forEach(p => counts[p.category] = (counts[p.category]||0)+1);
  let html = `<button data-cat="all" class="${state.cat==='all'?'active':''}">All aisles <span class="n">${ALL.products.length}</span></button>`;
  html += ALL.categories.map(c => `<button data-cat="${c.slug}" class="${state.cat===c.slug?'active':''}">${c.label} <span class="n">${counts[c.slug]||0}</span></button>`).join('');
  list.innerHTML = html;
  list.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
    state.cat = b.dataset.cat; renderFilters(); renderGrid();
  }));

  document.querySelectorAll('[data-stock]').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('[data-stock]').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    state.stock = b.dataset.stock; renderGrid();
  }));
}

function renderGrid(){
  const grid = document.getElementById('productGrid');
  const meta = document.getElementById('resultsMeta');
  let items = ALL.products.filter(p => {
    if (state.cat !== 'all' && p.category !== state.cat) return false;
    if (state.stock === 'in' && p.stock !== 'in') return false;
    if (state.q && !p.name.toLowerCase().includes(state.q.toLowerCase())) return false;
    return true;
  });

  meta.textContent = `${items.length} product${items.length===1?'':'s'}${state.cat!=='all' ? ' in ' + labelFor(state.cat) : ''}`;

  if (items.length === 0){
    grid.innerHTML = '<div class="empty-state" style="grid-column:1/-1;">No products match yet — try another aisle, or call the store: this line may be in-store only for now.</div>';
    return;
  }

  grid.innerHTML = items.map((p, i) => {
    const imgId = 'img_' + i;
    return `
    <div class="product-card" data-name="${p.name.replace(/"/g,'&quot;')}" data-price="${p.price}" data-unit="${p.unit}" data-category="${p.category}">
      ${p.stock === 'out' ? '<span class="badge badge-out">Sold out</span>' : (p.note ? '<span class="badge badge-sale">' + p.note + '</span>' : '')}
      <div class="photo" data-open-modal>
        <img id="${imgId}" src="${guessImageUrls(p.name)[0]}" alt="${p.name}"
             data-candidates='${JSON.stringify(guessImageUrls(p.name)).replace(/'/g,"&#39;")}' data-attempt="1"
             onerror="tryNextImage(this,'${p.category}')" loading="lazy">
      </div>
      <h4 data-open-modal>${p.name}</h4>
      <div class="unit qty-readout">1 &times; ${p.unit}</div>
      <div class="qty-stepper">
        <button type="button" class="qminus">&minus;</button>
        <span class="qval">1</span>
        <button type="button" class="qplus">+</button>
      </div>
      <div class="price-row">
        <span class="price pval">$${p.price.toFixed(2)}</span>
        <button class="add-btn" ${p.stock==='out'?'disabled':''}>+</button>
      </div>
    </div>
  `; }).join('');

  grid.querySelectorAll('.product-card').forEach(card => {
    const name = card.dataset.name, price = parseFloat(card.dataset.price), unit = card.dataset.unit;
    const category = card.dataset.category, stock = card.dataset.name ? undefined : undefined;
    let qty = 1;
    const qvalEl = card.querySelector('.qval');
    const readoutEl = card.querySelector('.qty-readout');
    const priceEl = card.querySelector('.pval');
    function refresh(){
      qvalEl.textContent = qty;
      readoutEl.textContent = `${qty} \u00d7 ${unit}`;
      priceEl.textContent = '$' + (price * qty).toFixed(2);
    }
    card.querySelector('.qminus').addEventListener('click', (e) => { e.stopPropagation(); if (qty > 1){ qty--; refresh(); } });
    card.querySelector('.qplus').addEventListener('click', (e) => { e.stopPropagation(); qty++; refresh(); });
    card.querySelector('.add-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      addToCart({ name, price: price * qty, unit: `${qty} \u00d7 ${unit}` });
      qty = 1; refresh();
    });
    card.querySelectorAll('[data-open-modal]').forEach(el => {
      el.addEventListener('click', () => openProductModal({ name, price, unit, category, outOfStock: card.querySelector('.badge-out') !== null }));
    });
  });
}

document.addEventListener('khyber:data-ready', () => {
  const hash = decodeURIComponent(location.hash.replace('#',''));
  if (hash && ALL.categories.some(c=>c.slug===hash)) state.cat = hash;
  const params = new URLSearchParams(location.search);
  const q = params.get('q');
  if (q){ state.q = q; document.getElementById('searchInput').value = q; }
  renderFilters();
  renderGrid();
});

document.getElementById('searchInput').addEventListener('input', (e) => {
  state.q = e.target.value; renderGrid();
});
</script>
"""

write("products.html", head("Shop — Khyber Spice Invader", "Browse spices, daals, rice, ghee, snacks and more from Khyber Spice Invader, Royal Oak.", "products.html") + shop_body + FOOT.replace("</body>", shop_script + "</body>"))

# ------------------------------------------------------------------
# ABOUT
# ------------------------------------------------------------------
about_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Our Story</h1>
    <p class="lede">Twenty years of stocking the aisle every other supermarket forgets.</p>

    <div class="prose" style="max-width:70ch;">
      <p>We started this business in 2005, delivering to the unique and traditional grocery needs of migrants from different countries living in New Zealand. We specialise in selling premium quality food products across spices, lentils, rice, flour, packaged foods, frozen foods, cosmetics, and household products.</p>
      <p>We hope you have a hassle-free shopping experience. We are certified &ldquo;A&rdquo; for our store hygiene by the Auckland Council, and we take pride in maintaining a clean and hygienic shopping environment at both our stores.</p>
    </div>

    <h2 style="font-family:var(--font-display); font-size:26px; margin:52px 0 24px;">Visit Us</h2>
    <div class="locations-grid" style="grid-template-columns:1fr;">
      <div class="location-card">
        <h3>Khyber Spice Invader &mdash; Royal Oak</h3>
        <p>822 Manukau Road, Royal Oak, Auckland 1061, New Zealand</p>
        <p>Phone: <a href="tel:+6496251766" style="color:var(--turmeric);">09 625 1766</a></p>
        <iframe loading="lazy" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d797.5162421535671!2d174.776662!3d-36.91271099999995!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6d0d48a64510d8fd%3A0x107e1c7b774f3610!2sKyber+Spice+Invader+%26+Vege+Oasis!5e0!3m2!1sen!2s!4v1407750401782"></iframe>
      </div>
    </div>
  </div>
</section>
"""
write("about.html", head("About Us — Khyber Spice Invader", "Khyber Spice Invader has served Auckland's Indian, Sri Lankan, Pakistani, Iranian and Arabic communities since 2005.", "about.html") + about_body + FOOT)

# ------------------------------------------------------------------
# SHIPPING
# ------------------------------------------------------------------
shipping_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Shipping &amp; Delivery</h1>
    <p class="lede">We ship anywhere in New Zealand using reputed courier services. Rates are based on weight and calculated at checkout.</p>

    <div class="callout">Pickup from either store is always free.</div>

    <h2 style="font-family:var(--font-display); font-size:24px; margin:40px 0 16px;">Local Auckland &mdash; 1&ndash;2 working days</h2>
    <table class="rate-table">
      <tr><th>Weight</th><th>Price</th></tr>
      <tr><td>0&ndash;20kg</td><td>$8.00</td></tr>
      <tr><td>20&ndash;40kg</td><td>$30.00</td></tr>
      <tr><td>40&ndash;60kg</td><td>$60.00</td></tr>
    </table>

    <h2 style="font-family:var(--font-display); font-size:24px; margin:40px 0 16px;">Rest of North Island &mdash; 2&ndash;3 working days</h2>
    <table class="rate-table">
      <tr><th>Weight</th><th>Price</th></tr>
      <tr><td>0&ndash;15kg</td><td>$12.00</td></tr>
      <tr><td>15&ndash;25kg</td><td>$30.00</td></tr>
      <tr><td>25&ndash;35kg</td><td>$60.00</td></tr>
    </table>

    <h2 style="font-family:var(--font-display); font-size:24px; margin:40px 0 16px;">South Island &mdash; 3&ndash;4 working days</h2>
    <table class="rate-table">
      <tr><th>Weight</th><th>Price</th></tr>
      <tr><td>0&ndash;5kg</td><td>$15.00</td></tr>
      <tr><td>5&ndash;10kg</td><td>$30.00</td></tr>
      <tr><td>10&ndash;15kg</td><td>$60.00</td></tr>
    </table>
  </div>
</section>
"""
write("shipping.html", head("Shipping Information — Khyber Spice Invader", "Delivery rates for Khyber Spice Invader — nationwide shipping across New Zealand.", "shipping.html") + shipping_body + FOOT)

# ------------------------------------------------------------------
# CONTACT
# ------------------------------------------------------------------
contact_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Get In Touch</h1>
    <p class="lede">Questions about stock, bulk orders, or a phone order while online checkout is on the way &mdash; we're easiest to reach by phone.</p>

    <div class="story-grid">
      <div>
        <form class="contact-form" onsubmit="event.preventDefault(); alert('Thanks — this form is a placeholder until email delivery is connected.');">
          <div>
            <label for="name">Name</label>
            <input id="name" type="text" required>
          </div>
          <div>
            <label for="email">Email</label>
            <input id="email" type="email" required>
          </div>
          <div>
            <label for="message">Message</label>
            <textarea id="message" required></textarea>
          </div>
          <button class="btn btn-primary" type="submit" style="justify-self:flex-start;">Send message</button>
        </form>
      </div>
      <div class="ticket">
        <div class="row"><span>Phone</span><span><a href="tel:+6496251766">09 625 1766</a></span></div>
        <div class="row"><span>Phone (alt)</span><span><a href="tel:+6496241365">09 624 1365</a></span></div>
        <div class="row"><span>Email</span><span><a href="mailto:sales@khyberspice.co.nz">sales@khyberspice.co.nz</a></span></div>
        <div class="row"><span>Address</span><span>822 Manukau Rd, Royal Oak</span></div>
        <div class="row"><span>Hours</span><span>Mon&ndash;Sun, 9am&ndash;8:30pm</span></div>
        <div class="row"><span>Facebook</span><span><a href="https://www.facebook.com/people/Khyber-Spice-Invader-Royal-Oak/100056588722990/" target="_blank" rel="noopener">@khyberspiceroyaloak</a></span></div>
      </div>
    </div>
  </div>
</section>
"""
write("contact.html", head("Contact — Khyber Spice Invader", "Get in touch with Khyber Spice Invader, Royal Oak — phone, email and store hours.", "contact.html") + contact_body + FOOT)

# ------------------------------------------------------------------
# ACCOUNT
# ------------------------------------------------------------------
account_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Your Account</h1>
    <p class="lede">Sign in to save your details for checkout and, once it's live, track your orders.</p>
    <div id="accountPanel"></div>
  </div>
</section>
"""
write("account.html", head("Account — Khyber Spice Invader", "Sign in to your Khyber Spice Invader account.", "account.html") + account_body + FOOT)

# ------------------------------------------------------------------
# PRIVACY POLICY
# ------------------------------------------------------------------
privacy_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Privacy Policy</h1>
    <p class="lede">Last updated August 2026. This explains what information this website collects and what happens to it.</p>
    <div class="callout">This is a starting draft, not legal advice — see the note at the end before relying on it for a live business.</div>
    <div class="prose" style="max-width:70ch;">
      <h2>What we collect</h2>
      <p>If you create an account (via the Sign in / Account page), we collect the name and email address you provide. If you use the contact form, we collect whatever you type into it. If you browse the shop, your basket and colour theme preference are stored only in your own browser (localStorage) — not sent to us or anyone else.</p>

      <h2>How it's used</h2>
      <p>Account details are used to let you sign in and, once online ordering launches, to process and track orders. Contact form submissions are used only to respond to your enquiry. We do not sell or rent personal information to third parties.</p>

      <h2>Who else sees it</h2>
      <p>Account sign-in is handled by Netlify Identity (part of Netlify, our hosting provider) — they process account data on our behalf under their own privacy terms. Once online payment launches, card details will be handled entirely by Stripe; this site never sees or stores your card number.</p>

      <h2>Your rights</h2>
      <p>Under the Privacy Act 2020 (New Zealand), you can ask what personal information we hold about you, ask us to correct it, or ask us to delete your account. Contact <a href="mailto:sales@khyberspice.co.nz" style="color:var(--turmeric);">sales@khyberspice.co.nz</a> for any of this.</p>

      <h2>Cookies &amp; local storage</h2>
      <p>This site uses your browser's local storage (not tracking cookies) to remember your basket contents and colour theme between visits. This data stays on your device and isn't accessible to us.</p>

      <h2>Changes</h2>
      <p>If this policy changes, the "last updated" date at the top will change too.</p>
    </div>
  </div>
</section>
"""
write("privacy.html", head("Privacy Policy — Khyber Spice Invader", "How Khyber Spice Invader collects and uses information on this website.", "privacy.html") + privacy_body + FOOT)

# ------------------------------------------------------------------
# TERMS & CONDITIONS
# ------------------------------------------------------------------
terms_body = """
<section class="info-page">
  <div class="wrap">
    <h1>Terms &amp; Conditions</h1>
    <p class="lede">Last updated August 2026. The basics of using this website and buying from us.</p>
    <div class="callout">This is a starting draft, not legal advice — see the note at the end before relying on it for a live business.</div>
    <div class="prose" style="max-width:70ch;">
      <h2>About this site</h2>
      <p>This website is operated by Khyber Spice Invader, 822 Manukau Road, Royal Oak, Auckland 1061, New Zealand. Using this site means you accept these terms.</p>

      <h2>Product information</h2>
      <p>We do our best to keep prices, descriptions and stock status accurate, but items can sell out or change price in-store faster than the website updates. If anything here doesn't match what's in-store, the in-store price and availability is what applies — please call us on 09 625 1766 to confirm before making a special trip for something specific.</p>

      <h2>Online ordering</h2>
      <p>Online checkout is not yet live on this site. Adding items to your basket does not place an order — for now, use it as a shopping list and call the store to arrange purchase or delivery. Once online payment (via Stripe) launches, separate checkout terms covering payment, delivery timing and cancellation will be added here.</p>

      <h2>Your consumer rights</h2>
      <p>Nothing in these terms limits your rights under the Consumer Guarantees Act 1993 or the Fair Trading Act 1986. Goods you buy from us, in-store or online, come with guarantees that can't be excluded under New Zealand law.</p>

      <h2>Shipping</h2>
      <p>See the <a href="shipping.html" style="color:var(--turmeric);">Shipping page</a> for current delivery rates and timeframes by region.</p>

      <h2>Liability</h2>
      <p>This website is provided as-is. We're not liable for indirect or consequential loss arising from use of the site, to the extent permitted by law — this doesn't affect your statutory rights above.</p>

      <h2>Contact</h2>
      <p>Questions about these terms: <a href="mailto:sales@khyberspice.co.nz" style="color:var(--turmeric);">sales@khyberspice.co.nz</a> or 09 625 1766.</p>
    </div>
  </div>
</section>
"""
write("terms.html", head("Terms & Conditions — Khyber Spice Invader", "Terms and conditions for using the Khyber Spice Invader website.", "terms.html") + terms_body + FOOT)

# ------------------------------------------------------------------
# PHOTO MANIFEST — exact filenames the local-override system checks,
# so adding real photos is just "save file with this exact name".
# ------------------------------------------------------------------
import json as _json, re as _re
_catalog = _json.load(open(os.path.join(ROOT, "data", "products.json")))
_lines = [
    "# Product photo filenames",
    "",
    "Every product below first checks assets/products/<filename> before",
    "anything else. Save a real photo with the EXACT filename shown (jpg",
    "or png both work) and it will appear on the site immediately — no",
    "code changes, no rebuild, just refresh the page.",
    "",
]
for p in _catalog["products"]:
    slug = _re.sub(r'^-+|-+$', '', _re.sub(r'[^a-z0-9]+', '-', p["name"].lower()))
    _lines.append(f'{p["name"]:<45} -> assets/products/{slug}.jpg')
os.makedirs(os.path.join(ROOT, "assets", "products"), exist_ok=True)
with open(os.path.join(ROOT, "assets", "products", "PHOTO_FILENAMES.txt"), "w") as f:
    f.write("\n".join(_lines) + "\n")
print("wrote assets/products/PHOTO_FILENAMES.txt")

print("\\nBuild complete.")
