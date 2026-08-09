// ============================================================
// Ambient "spices sifting down" canvas animation for the hero.
// This is an original generative effect rather than stock video
// footage — no licence to verify, and it's tuned to the site's
// exact palette. Runs at low opacity so it reads as atmosphere,
// not a distraction. Respects prefers-reduced-motion.
// ============================================================

(function(){
  const canvas = document.getElementById('spiceCanvas');
  if (!canvas) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');
  const COLORS = ['255,182,39', '255,90,54', '111,207,110', '155,126,240'];
  let w, h, particles;

  function resize(){
    w = canvas.width = canvas.offsetWidth * devicePixelRatio;
    h = canvas.height = canvas.offsetHeight * devicePixelRatio;
  }

  function makeParticle(spawnAtTop){
    const r = (2 + Math.random() * 4) * devicePixelRatio;
    return {
      x: Math.random() * w,
      y: spawnAtTop ? -20 : Math.random() * h,
      r,
      speed: (0.25 + Math.random() * 0.6) * devicePixelRatio,
      drift: (Math.random() - 0.5) * 0.4 * devicePixelRatio,
      wobble: Math.random() * Math.PI * 2,
      wobbleSpeed: 0.01 + Math.random() * 0.02,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      alpha: 0.12 + Math.random() * 0.22,
    };
  }

  function init(){
    resize();
    const count = Math.min(70, Math.floor((w * h) / 90000));
    particles = Array.from({ length: count }, () => makeParticle(false));
  }

  function tick(){
    ctx.clearRect(0, 0, w, h);
    particles.forEach(p => {
      p.y += p.speed;
      p.wobble += p.wobbleSpeed;
      p.x += p.drift + Math.sin(p.wobble) * 0.3;
      if (p.y - p.r > h){ Object.assign(p, makeParticle(true)); }
      if (p.x < -10) p.x = w + 10;
      if (p.x > w + 10) p.x = -10;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color},${p.alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', resize);
  init();
  requestAnimationFrame(tick);
})();
