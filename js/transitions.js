// ============================================================
// Page transition — clicking an internal nav link grows the
// destination's name to fill the screen before navigating; on
// arrival the incoming page's name shrinks away to reveal the
// content underneath. Pure CSS transform/opacity, no framework.
// ============================================================

const PAGE_LABELS = {
  'index.html': 'Home', '': 'Home',
  'products.html': 'Shop',
  'about.html': 'About',
  'shipping.html': 'Shipping',
  'contact.html': 'Contact',
  'account.html': 'Account',
};

function pageLabelFromHref(href){
  const file = href.split('#')[0].split('?')[0].split('/').pop();
  return PAGE_LABELS[file] || 'Khyber';
}

(function(){
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const overlay = document.createElement('div');
  overlay.className = 'page-transition';
  overlay.innerHTML = '<span class="pt-text"></span>';
  document.body.appendChild(overlay);
  const textEl = overlay.querySelector('.pt-text');

  // Reveal animation on arrival: cover instantly, then shrink+fade away.
  const currentLabel = pageLabelFromHref(location.pathname);
  textEl.textContent = currentLabel;
  overlay.style.transition = 'none';
  textEl.style.transition = 'none';
  overlay.style.opacity = '1';
  overlay.style.pointerEvents = 'auto';
  textEl.style.transform = 'scale(1)';
  // force reflow so the "none" transition actually applies before we re-enable it
  overlay.offsetHeight;
  overlay.style.transition = '';
  textEl.style.transition = '';

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      overlay.style.opacity = '0';
      overlay.style.pointerEvents = 'none';
      textEl.style.transform = 'scale(0.55)';
    });
  });

  // Intercept internal page links for the "leaving" animation.
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    const href = a.getAttribute('href') || '';
    const isInternalPage = /\.html($|#|\?)/.test(href) && !href.startsWith('http') && a.target !== '_blank';
    if (!isInternalPage || e.metaKey || e.ctrlKey || e.shiftKey) return;

    e.preventDefault();
    textEl.textContent = pageLabelFromHref(href);
    overlay.style.transition = 'none';
    textEl.style.transition = 'none';
    overlay.style.opacity = '0';
    textEl.style.transform = 'scale(0.7)';
    overlay.offsetHeight;
    overlay.style.transition = '';
    textEl.style.transition = '';

    requestAnimationFrame(() => {
      overlay.style.opacity = '1';
      overlay.style.pointerEvents = 'auto';
      textEl.style.transform = 'scale(2.3)';
    });

    setTimeout(() => { window.location.href = href; }, 480);
  });
})();
