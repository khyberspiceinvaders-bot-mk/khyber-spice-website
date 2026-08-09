// ============================================================
// Khyber Spice Invader — site-wide behaviour
// Cart is stored in localStorage. No payment processing yet —
// this is wired for a Stripe Checkout integration to be dropped
// in later (see README "Adding Stripe").
// ============================================================

const CART_KEY = 'khyber_cart_v1';

function tryNextImage(img, category){
  const urls = JSON.parse(img.dataset.candidates || '[]');
  const attempt = parseInt(img.dataset.attempt || '0');
  if (attempt < urls.length){
    img.dataset.attempt = attempt + 1;
    img.src = urls[attempt];
  } else {
    img.replaceWith(iconFallback(category));
  }
}
function smartImg(name, category, extraAttrs){
  const urls = guessImageUrls(name);
  return `<img src="${urls[0]}" alt="${name}" loading="lazy" data-candidates='${JSON.stringify(urls).replace(/'/g,"&#39;")}' data-attempt="1" onerror="tryNextImage(this,'${category}')" ${extraAttrs||''}>`;
}

// Guess the live product photo URL from the original store's predictable
// CDN naming pattern. Several filename variants are tried in sequence
// (see data-attempt wiring in shop.js) before falling back to a
// designed icon card — so a wrong guess never shows broken art, and
// coverage is maximised without needing per-product manual images.
function guessImageUrls(name){
  const slug = name.toUpperCase().replace(/[^A-Z0-9]+/g, '_').replace(/^_+|_+$/g, '');
  const base = 'https://www.khyberspice.co.nz/cdn/shop/products/';
  return [
    base + slug + '_medium.jpg',
    base + slug + '.jpg',
    base + slug + '_grande.jpg',
    base + slug + '_large.jpg',
  ];
}

function getCart(){
  try{ return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
  catch(e){ return []; }
}
function saveCart(cart){
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  renderCartCount();
  renderCartDrawer();
}
function addToCart(product){
  const cart = getCart();
  const existing = cart.find(i => i.name === product.name);
  if (existing) existing.qty += 1;
  else cart.push({ name: product.name, price: product.price, unit: product.unit, qty: 1 });
  saveCart(cart);
  openCart();
}
function removeFromCart(name){
  saveCart(getCart().filter(i => i.name !== name));
}
function cartTotal(cart){
  return cart.reduce((sum, i) => sum + i.price * i.qty, 0);
}
function fmt(n){ return '$' + n.toFixed(2); }

function renderCartCount(){
  const el = document.getElementById('cartCount');
  if (!el) return;
  const count = getCart().reduce((s,i)=>s+i.qty,0);
  el.textContent = count;
  el.style.display = count > 0 ? 'flex' : 'none';
}

function renderCartDrawer(){
  const itemsEl = document.getElementById('cartItems');
  const totalEl = document.getElementById('cartTotal');
  if (!itemsEl) return;
  const cart = getCart();
  if (cart.length === 0){
    itemsEl.innerHTML = '<div class="empty-state">Your basket is empty.<br>Browse the shop to add items.</div>';
  } else {
    itemsEl.innerHTML = cart.map(i => `
      <div class="cart-line">
        <div>
          <div class="name">${i.name}</div>
          <div class="qty">${i.qty} × ${fmt(i.price)} / ${i.unit}</div>
        </div>
        <button class="remove" onclick="removeFromCart('${i.name.replace(/'/g,"\\'")}')">Remove</button>
      </div>
    `).join('');
  }
  if (totalEl) totalEl.innerHTML = `<span>Subtotal</span><strong>${fmt(cartTotal(cart))}</strong>`;
}

function openCart(){
  document.getElementById('cartDrawer')?.classList.add('open');
  document.getElementById('cartOverlay')?.classList.add('open');
}
function closeCart(){
  document.getElementById('cartDrawer')?.classList.remove('open');
  document.getElementById('cartOverlay')?.classList.remove('open');
}

document.addEventListener('DOMContentLoaded', () => {
  renderCartCount();
  renderCartDrawer();

  document.getElementById('navToggle')?.addEventListener('click', () => {
    document.getElementById('mainNav')?.classList.toggle('open');
  });
  document.getElementById('cartToggle')?.addEventListener('click', openCart);
  document.getElementById('cartClose')?.addEventListener('click', closeCart);
  document.getElementById('cartOverlay')?.addEventListener('click', closeCart);

  const headerSearch = document.getElementById('headerSearchInput');
  headerSearch?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && headerSearch.value.trim()){
      location.href = 'products.html?q=' + encodeURIComponent(headerSearch.value.trim());
    }
  });

  // ---- Theme switcher ----
  const themeToggle = document.getElementById('themeToggle');
  const themePopover = document.getElementById('themePopover');
  const themeTeaser = document.getElementById('themeTeaser');
  const themeDot = document.getElementById('themeDot');
  const savedTheme = localStorage.getItem('khyber_theme') || 'khyber';

  if (!localStorage.getItem('khyber_theme_seen')){
    setTimeout(() => { themeTeaser?.classList.add('show'); }, 1200);
    setTimeout(() => { themeTeaser?.classList.remove('show'); }, 9000);
  } else {
    themeDot?.remove();
  }

  document.querySelectorAll('.theme-option').forEach(btn => {
    if (btn.dataset.theme === savedTheme) btn.classList.add('active');
    btn.addEventListener('click', () => {
      const t = btn.dataset.theme;
      if (t === 'khyber') document.documentElement.removeAttribute('data-theme');
      else document.documentElement.setAttribute('data-theme', t);
      localStorage.setItem('khyber_theme', t);
      localStorage.setItem('khyber_theme_seen', '1');
      themeDot?.remove();
      document.querySelectorAll('.theme-option').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
  themeToggle?.addEventListener('click', (e) => {
    e.stopPropagation();
    themeTeaser?.classList.remove('show');
    localStorage.setItem('khyber_theme_seen', '1');
    themeDot?.remove();
    themePopover?.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (themePopover?.classList.contains('open') && !themePopover.contains(e.target) && e.target !== themeToggle){
      themePopover.classList.remove('open');
    }
  });
});
