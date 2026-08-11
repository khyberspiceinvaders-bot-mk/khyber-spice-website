// ============================================================
// Auth — wired to Netlify Identity, a real free auth service
// built into Netlify. No custom backend needed. To activate:
// Netlify dashboard → Site configuration → Identity → Enable Identity.
// The "Account" nav link always works as a normal link to
// account.html, which shows a sign-in card when logged out —
// no separate header button needed.
// ============================================================

function initAuthUI(){
  const widget = window.netlifyIdentity;
  const navLink = document.getElementById('accountNavLink');

  function reflectUser(user){
    if (navLink) navLink.textContent = user ? (user.user_metadata?.full_name || 'Account').split(' ')[0] : 'Account';
    const accEl = document.getElementById('accountPanel');
    if (accEl) renderAccountPanel(user);
  }

  if (!widget) return; // Identity script didn't load — account.html's own card still explains what to do.

  widget.on('init', reflectUser);
  widget.on('login', user => { reflectUser(user); widget.close(); });
  widget.on('logout', () => reflectUser(null));
  widget.init();
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
