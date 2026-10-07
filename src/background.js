// A procedural Data Swallow-inspired network tunnel; no game footage or assets.
(() => {
  'use strict';
  const canvas = document.getElementById('electrosphere');
  const toggle = document.getElementById('motion');
  if (!canvas || !window.CanvasRenderingContext2D) return;
  const ctx = canvas.getContext('2d', {alpha: false});
  if (!ctx) return;
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const storageKey = 'ac3-jp-background-motion';
  let paused = preference.matches;
  try { paused ||= localStorage.getItem(storageKey) === 'paused'; } catch (_) {}
  let width = 0, height = 0, elapsed = 0, request = 0, previous = 0;
  const sides = 16, depth = 34, spacing = 1.25;

  function ring(z, distance) {
    const scale = Math.min(width, height) * .93 / (z + .8);
    const bendX = (Math.sin(distance * .16) - Math.sin((distance-z) * .16)) * 1.4;
    const bendY = (Math.cos(distance * .12) - Math.cos((distance-z) * .12)) * .9;
    const twist = Math.sin(distance * .08) * .18;
    return Array.from({length: sides}, (_, i) => {
      const angle = i * Math.PI * 2 / sides + twist;
      return [width * .63 + (Math.cos(angle) * 3.4 + bendX) * scale,
              height * .58 + (Math.sin(angle) * 3.4 + bendY) * scale];
    });
  }

  function draw() {
    ctx.fillStyle = '#e5e7dc';
    ctx.fillRect(0, 0, width, height);
    const travel = elapsed * .65, phase = travel % spacing;
    let far = ring(depth * spacing - phase, depth * spacing + travel - phase);
    for (let j = depth-1; j >= 0; j--) {
      const z = j * spacing - phase;
      if (z < .15) continue;
      const near = ring(z, z + travel);
      for (let i = 0; i < sides; i++) {
        const k = (i+1) % sides;
        const points = [near[i], near[k], far[k], far[i]];
        if (points.every(p => p[0] < 0) || points.every(p => p[0] > width) ||
            points.every(p => p[1] < 0) || points.every(p => p[1] > height)) continue;
        const band = (j + Math.floor(travel/spacing)) % 4 === 0 ? -1.6 : 0;
        const light = 85 + Math.cos(i * Math.PI * 2 / sides - .6) * 5 + j/depth * 5 + band;
        ctx.beginPath();
        points.forEach((p, index) => index ? ctx.lineTo(...p) : ctx.moveTo(...p));
        ctx.closePath();
        ctx.fillStyle = `hsl(62 24% ${light}%)`;
        ctx.fill();
        ctx.strokeStyle = 'rgba(100,108,64,.12)';
        ctx.lineWidth = .7;
        ctx.stroke();
      }
      far = near;
    }
  }

  function frame(stamp) {
    request = 0;
    if (paused || document.hidden) return;
    if (!previous) previous = stamp;
    if (stamp-previous >= 1000/30) {
      elapsed += Math.min((stamp-previous)/1000, .1);
      previous = stamp;
      draw();
    }
    request = requestAnimationFrame(frame);
  }

  function sync() {
    cancelAnimationFrame(request);
    previous = 0;
    canvas.dataset.motion = paused ? 'paused' : 'running';
    if (toggle) {
      toggle.hidden = false;
      toggle.textContent = paused ? 'Play background' : 'Pause background';
      toggle.setAttribute('aria-pressed', String(paused));
    }
    if (!paused && !document.hidden) request = requestAnimationFrame(frame);
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
  }

  toggle?.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem(storageKey, paused ? 'paused' : 'running'); } catch (_) {}
    sync();
  });
  preference.addEventListener('change', event => { paused = event.matches; sync(); });
  document.addEventListener('visibilitychange', sync);
  window.addEventListener('resize', resize, {passive: true});
  resize();
  sync();
})();
