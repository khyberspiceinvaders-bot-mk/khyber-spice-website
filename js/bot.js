// ============================================================
// Khyber Bot — lightweight rule-based assistant.
// Answers common questions instantly from store data; anything
// it doesn't recognise gets handed off as a pre-filled email to
// sales@khyberspice.co.nz so a real person follows up.
// (Not a hosted AI model — this runs entirely in the browser,
// no API key or backend needed. Swap in a real LLM later by
// replacing answerQuery() with an API call.)
// ============================================================

const BOT_FAQ = [
  { keys: ['hour', 'open', 'close', 'time'], a: "We're open every day, 9:00am to 8:30pm, at both stores." },
  { keys: ['where', 'address', 'location', 'royal oak', 'otahuhu', 'ōtāhuhu'], a: "Royal Oak: 822 Manukau Road, Auckland. Ōtāhuhu: 539 Great South Road, Auckland. Both on the About page with maps." },
  { keys: ['deliver', 'shipping', 'ship', 'courier'], a: "We ship anywhere in New Zealand — rates depend on weight and region, see the Shipping page for the full table. Pickup from either store is always free." },
  { keys: ['phone', 'call', 'contact', 'number'], a: "You can call us on 09 625 1766 or 09 624 1365, or email sales@khyberspice.co.nz." },
  { keys: ['stripe', 'pay', 'payment', 'checkout', 'card online', 'buy online'], a: "Online checkout is being set up right now — for the moment, add items to your basket and call the store to place the order over the phone." },
  { keys: ['spice'], a: "We stock a big range of whole and ground spices — head to the Shop page and filter by \"Spices\" to browse." },
  { keys: ['rice', 'basmati'], a: "We carry basmati rice from 1kg bags up to 20kg sacks, plus besan, maida and specialty flours — see \"Rice & Flour\" in the Shop." },
  { keys: ['daal', 'dal', 'lentil', 'bean'], a: "Daals, lentils and beans are all under the \"Daals & Lentils\" aisle on the Shop page." },
  { keys: ['account', 'sign in', 'sign up', 'login', 'log in', 'register'], a: "You can create an account or sign in from the button in the top corner — handy for when order tracking goes live." },
  { keys: ['hi', 'hello', 'hey'], a: "Hey! I'm the Khyber Bot. Ask me about hours, delivery, locations, or what's in stock." },
];

function answerQuery(q){
  const lower = q.toLowerCase();
  for (const item of BOT_FAQ){
    if (item.keys.some(k => lower.includes(k))) return { text: item.a, handled: true };
  }
  return {
    text: "I'm not sure on that one — want me to send it straight to the team? Tap \"Email the store\" below and I'll prefill it for you.",
    handled: false
  };
}

function botAddMessage(text, who){
  const wrap = document.getElementById('botMessages');
  if (!wrap) return;
  const div = document.createElement('div');
  div.className = 'bot-msg ' + who;
  div.textContent = text;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function botHandle(query){
  if (!query.trim()) return;
  botAddMessage(query, 'user');
  const { text, handled } = answerQuery(query);
  setTimeout(() => {
    botAddMessage(text, 'bot');
    if (!handled){
      const wrap = document.getElementById('botMessages');
      const btn = document.createElement('a');
      btn.href = `mailto:sales@khyberspice.co.nz?subject=Question from website chat&body=${encodeURIComponent(query)}`;
      btn.className = 'btn btn-outline btn-small';
      btn.style.alignSelf = 'flex-start';
      btn.textContent = 'Email the store';
      wrap.appendChild(btn);
      wrap.scrollTop = wrap.scrollHeight;
    }
  }, 350);
}

document.addEventListener('DOMContentLoaded', () => {
  const launcher = document.getElementById('botLauncher');
  const panel = document.getElementById('botPanel');
  const closeBtn = document.getElementById('botClose');
  const input = document.getElementById('botInput');
  const sendBtn = document.getElementById('botSend');

  launcher?.addEventListener('click', () => {
    panel?.classList.toggle('open');
    if (panel?.classList.contains('open') && document.getElementById('botMessages')?.children.length === 0){
      botAddMessage("Hi, I'm the Khyber Bot 👋 Ask me about hours, delivery, locations or stock — I'll email the team for anything trickier.", 'bot');
    }
  });
  closeBtn?.addEventListener('click', () => panel?.classList.remove('open'));

  sendBtn?.addEventListener('click', () => { botHandle(input.value); input.value = ''; });
  input?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter'){ botHandle(input.value); input.value = ''; }
  });

  document.querySelectorAll('.bot-suggestions button').forEach(b => {
    b.addEventListener('click', () => botHandle(b.textContent));
  });
});
