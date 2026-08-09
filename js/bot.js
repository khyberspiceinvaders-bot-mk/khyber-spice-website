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
  { keys: ['hour', 'open', 'close', 'time'], a: "We're open every day, 9:00am to 8:30pm." },
  { keys: ['where', 'address', 'location', 'royal oak'], a: "We're at 822 Manukau Road, Royal Oak, Auckland — see the About page for the map." },
  { keys: ['deliver', 'shipping', 'ship', 'courier'], a: "We ship anywhere in New Zealand — rates depend on weight and region, see the Shipping page for the full table. Pickup from the store is always free." },
  { keys: ['phone', 'call', 'contact', 'number'], a: "You can call us on 09 625 1766 or 09 624 1365, or email sales@khyberspice.co.nz." },
  { keys: ['stripe', 'pay', 'payment', 'checkout', 'card online', 'buy online'], a: "Online checkout is being set up right now — for the moment, add items to your basket and call the store to place the order over the phone." },
  { keys: ['spice'], a: "We stock a big range of whole and ground spices — head to the Shop page and filter by \"Spices\" to browse." },
  { keys: ['account', 'sign in', 'sign up', 'login', 'log in', 'register'], a: "You can create an account or sign in from the button in the top corner — handy for when order tracking goes live." },
  { keys: ['hi', 'hello', 'hey'], a: "Hey! I'm the Khyber Bot. Ask me about hours, delivery, locations, stock, or even cooking questions like what to pair with a dish." },

  // ---- Cooking & pairing knowledge ----
  { keys: ['pair', 'goes with', 'go with', 'serve with'],
    a: "Yellow daal (moong or masoor) pairs best with plain steamed basmati, or jeera (cumin) rice for extra aroma. Thicker daals like chana or urad hold up well against pulao or a heartier long-grain rice. A squeeze of lemon and a tadka of ghee, cumin and dried red chilli over the top finishes it nicely." },
  { keys: ['cook rice', 'cooking rice', 'how to cook rice', 'boil rice'],
    a: "For basmati: rinse until the water runs clear, soak 20–30 min if you have time. Ratio is about 1 cup rice to 1.5 cups water. Bring to a boil, then cover and simmer on low for 12–15 minutes, off heat resting 5 minutes before fluffing. For older or thicker grain rice, closer to 1:2 water works better." },
  { keys: ['cook daal', 'cooking daal', 'cook dal', 'how long daal', 'daal time'],
    a: "Split, hulled daals like moong or masoor cook fastest — about 20–25 minutes at a simmer, no soaking needed. Whole daals or chana dal benefit from a 1–2 hour soak first, then 30–40 minutes simmering (or about 15–20 minutes in a pressure cooker)." },
  { keys: ['tadka', 'tempering', 'chaunk'],
    a: "A basic tadka: heat 2 tbsp ghee or oil, add cumin seeds until they sizzle, then mustard seeds, a dried red chilli, and a few curry leaves if you have them. Pour hot over your daal or sabzi right before serving." },
  { keys: ['basmati', 'best rice'],
    a: "For everyday meals, a mid-range basmati like India Gate Classic is reliable. For biryani or when you want extra-long, separate grains, go for an aged basmati — the Sahara or Qataghan Sela bags are good for that." },
  { keys: ['garam masala'],
    a: "Garam masala is best added near the end of cooking, off heat or in the last couple of minutes — it's an aromatic finishing spice blend rather than a base one, so early cooking burns off its fragrance." },
  { keys: ['store spices', 'keep spices fresh', 'spice storage'],
    a: "Keep spices in airtight containers, away from direct light and away from the stove's heat — whole spices keep their potency far longer than pre-ground ones, often a year or more versus a few months." },

  // ---- Product location (kept general, checked after the cooking-specific ones above) ----
  { keys: ['rice'], a: "We carry basmati rice from 1kg bags up to 20kg sacks, plus besan, maida and specialty flours — see \"Rice & Flour\" in the Shop." },
  { keys: ['daal', 'dal', 'lentil', 'bean'], a: "Daals, lentils and beans are all under the \"Daals & Lentils\" aisle on the Shop page." },
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
  const teaser = document.getElementById('botTeaser');
  const teaserClose = document.getElementById('botTeaserClose');

  // Show a one-time teaser bubble a few seconds after arrival, so the
  // bot doesn't rely on people noticing a small icon.
  if (!sessionStorage.getItem('khyber_bot_teaser_shown')){
    setTimeout(() => { teaser?.classList.add('show'); }, 3500);
    setTimeout(() => { teaser?.classList.remove('show'); }, 12000);
    sessionStorage.setItem('khyber_bot_teaser_shown', '1');
  }
  teaserClose?.addEventListener('click', () => teaser?.classList.remove('show'));

  launcher?.addEventListener('click', () => {
    teaser?.classList.remove('show');
    panel?.classList.toggle('open');
    if (panel?.classList.contains('open') && document.getElementById('botMessages')?.children.length === 0){
      botAddMessage("Hi, I'm the Khyber Bot 👋 Ask me about hours, delivery, locations, stock — or cooking questions like \"what goes well with yellow daal\". I'll email the team for anything trickier.", 'bot');
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
