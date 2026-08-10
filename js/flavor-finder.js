// ============================================================
// Flavor Finder — a 3-question quiz that recommends real
// products from the catalog. Not on the original site; built
// as a distinctive, genuinely useful feature rather than a
// visual gimmick.
// ============================================================

const FF_QUESTIONS = [
  {
    q: "What are you cooking tonight?",
    options: [
      { label: "Daal & rice", cats: ['daals-lentils','rice-flour'] },
      { label: "A spiced-up curry", cats: ['spices','ghee-oil'] },
      { label: "Snacks & chai", cats: ['snacks','beverages'] },
      { label: "Not sure yet", cats: ['spices','daals-lentils'] },
    ]
  },
  {
    q: "How much heat do you like?",
    options: [
      { label: "Keep it mild", cats: ['personal-care','beverages'] },
      { label: "Medium, please", cats: ['spices','pickles-chutney'] },
      { label: "Bring the heat", cats: ['spices','pickles-chutney'] },
    ]
  },
  {
    q: "Pick a vibe",
    options: [
      { label: "Comfort classic", cats: ['daals-lentils','rice-flour'] },
      { label: "Something new to try", cats: ['subcontinental','misc-grocery'] },
      { label: "Quick and easy", cats: ['instant-food','snacks'] },
    ]
  }
];

let ffAnswers = [];
let ffStep = 0;

function ffRenderQuestion(){
  const modal = document.getElementById('ffModal');
  const step = FF_QUESTIONS[ffStep];
  modal.innerHTML = `
    <button class="ff-close" id="ffClose" aria-label="Close">&times;</button>
    <div class="ff-progress">
      ${FF_QUESTIONS.map((_,i) => `<span class="${i <= ffStep ? 'done' : ''}"></span>`).join('')}
    </div>
    <div class="ff-q">${step.q}</div>
    <div class="ff-options">
      ${step.options.map((o,i) => `<button type="button" data-i="${i}">${o.label}</button>`).join('')}
    </div>
  `;
  modal.querySelector('#ffClose').addEventListener('click', ffClose);
  modal.querySelectorAll('.ff-options button').forEach(b => {
    b.addEventListener('click', () => {
      ffAnswers.push(step.options[parseInt(b.dataset.i)]);
      ffStep++;
      if (ffStep < FF_QUESTIONS.length) ffRenderQuestion();
      else ffRenderResult();
    });
  });
}

function ffRenderResult(){
  const modal = document.getElementById('ffModal');
  // Tally category votes across all three answers, pick the winner.
  const tally = {};
  ffAnswers.forEach(a => a.cats.forEach(c => { tally[c] = (tally[c]||0) + 1; }));
  const topCat = Object.entries(tally).sort((a,b) => b[1]-a[1])[0][0];
  const catInfo = ALL.categories.find(c => c.slug === topCat) || {};
  let picks = ALL.products.filter(p => p.category === topCat && p.stock === 'in');
  if (picks.length < 3){
    const secondCat = Object.entries(tally).sort((a,b) => b[1]-a[1])[1];
    if (secondCat) picks = picks.concat(ALL.products.filter(p => p.category === secondCat[0] && p.stock === 'in'));
  }
  picks = picks.slice(0, 3);

  modal.innerHTML = `
    <button class="ff-close" id="ffClose" aria-label="Close">&times;</button>
    <div class="ff-result-head">
      <span class="emoji">&#127881;</span>
      <h3>Your flavor match: ${catInfo.label || 'Pantry Essentials'}</h3>
      <p>${catInfo.blurb || "Here's a starting point pulled from real stock."}</p>
    </div>
    <div class="ff-result-grid">
      ${picks.map(p => `
        <div class="ff-result-item" data-name="${p.name.replace(/"/g,'&quot;')}" data-price="${p.price}" data-unit="${p.unit}" data-category="${p.category}">
          <div class="photo">${smartImg(p.name, p.category)}</div>
          <div class="rn">${p.name}</div>
          <div class="rp">$${p.price.toFixed(2)}</div>
        </div>
      `).join('')}
    </div>
    <button class="btn btn-primary" style="width:100%; justify-content:center;" id="ffAddAll">Add these to basket</button>
    <button class="btn btn-outline btn-small" style="width:100%; justify-content:center; margin-top:10px;" id="ffRetry">Try again</button>
  `;
  modal.querySelector('#ffClose').addEventListener('click', ffClose);
  modal.querySelector('#ffRetry').addEventListener('click', ffStart);
  modal.querySelector('#ffAddAll').addEventListener('click', () => {
    picks.forEach(p => addToCart({ name: p.name, price: p.price, unit: p.unit }));
    ffClose();
    openCart();
  });
  modal.querySelectorAll('.ff-result-item').forEach(el => {
    el.addEventListener('click', () => {
      ffClose();
      openProductModal({ name: el.dataset.name, price: parseFloat(el.dataset.price), unit: el.dataset.unit, category: el.dataset.category, outOfStock: false });
    });
  });
}

function ffStart(){
  ffAnswers = []; ffStep = 0;
  ffRenderQuestion();
}
function ffClose(){
  document.getElementById('ffOverlay')?.classList.remove('open');
}

document.addEventListener('DOMContentLoaded', () => {
  const trigger = document.getElementById('ffTrigger');
  trigger?.addEventListener('click', () => {
    document.getElementById('ffOverlay')?.classList.add('open');
    if (ALL.products.length) ffStart();
    else document.addEventListener('khyber:data-ready', ffStart, { once: true });
  });
  document.getElementById('ffOverlay')?.addEventListener('click', (e) => {
    if (e.target.id === 'ffOverlay') ffClose();
  });
});
