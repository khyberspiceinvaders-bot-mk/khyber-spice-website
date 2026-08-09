// ============================================================
// Auth — wired to Netlify Identity, a real free auth service
// built into Netlify. No custom backend needed. To activate:
// Netlify dashboard → Site configuration → Identity → Enable Identity.
// Until enabled, the sign-in button still opens but auth calls
// will no-op gracefully.
// ============================================================

function initAuthUI(){
  const widget = window.netlifyIdentity;
  const signInBtn = document.getElementById('signInBtn');
  const accountName = document.getElementById('accountName');

  function reflectUser(user){
    if (accountName) accountName.textContent = user ? (user.user_metadata?.full_name || user.email) : '';
    if (signInBtn) signInBtn.textContent = user ? 'Account' : 'Sign in';
    const accEl = document.getElementById('accountPanel');
    if (accEl) renderAccountPanel(user);
  }

  if (!widget){
    // Identity script didn't load (e.g. offline preview) — degrade gracefully.
    signInBtn?.addEventListener('click', () => alert('Sign-in requires Netlify Identity to be enabled on the deployed site.'));
    return;
  }

  widget.on('init', reflectUser);
  widget.on('login', user => { reflectUser(user); widget.close(); });
  widget.on('logout', () => reflectUser(null));
  widget.init();

  signInBtn?.addEventListener('click', () => {
    const user = widget.currentUser();
    if (user && location.pathname.indexOf('account.html') === -1){
      location.href = 'account.html';
    } else {
      widget.open(user ? undefined : 'login');
    }
  });
}

function renderAccountPanel(user){
  const el = document.getElementById('accountPanel');
  if (!el) return;
  if (!user){
    el.innerHTML = `
      <div class="account-card">
        <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 10px;">You're not signed in</h3>
        <p style="color:var(--paper-dim); font-size:14px; margin:0 0 20px;">Create an account to save your details for checkout once it launches, and to track orders after that.</p>
        <button class="btn btn-primary" onclick="window.netlifyIdentity && window.netlifyIdentity.open('login')">Sign in / Create account</button>
      </div>`;
    return;
  }
  const name = user.user_metadata?.full_name || user.email.split('@')[0];
  el.innerHTML = `
    <div class="account-card">
      <div class="avatar">${name.charAt(0).toUpperCase()}</div>
      <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 4px;">${name}</h3>
      <p style="color:var(--paper-dim); font-size:13.5px; margin:0 0 24px;">${user.email}</p>
      <div class="callout" style="margin:0 0 20px;">Order tracking will appear here once online checkout (via Stripe) is live. For now, call the store to check on a phone order.</div>
      <button class="btn btn-outline btn-small" onclick="window.netlifyIdentity && window.netlifyIdentity.logout()">Sign out</button>
    </div>`;
}

document.addEventListener('DOMContentLoaded', initAuthUI);
