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
  let width = 0, height = 0, ratio = 0, elapsed = 0, request = 0;
  let previous = null, lastDraw = 0;
  const sides = 24, depth = 34, spacing = 1.25, speed = 7.5;

  function ring(z) {
    const scale = Math.min(width, height) * .93 / (z + .8);
    return Array.from({length: sides}, (_, i) => {
      const angle = i * Math.PI * 2 / sides;
      return [width * .56 + Math.cos(angle) * 4.6 * scale,
              height * .48 + Math.sin(angle) * 3 * scale];
    });
  }

  function draw() {
    ctx.fillStyle = '#e5e7dc';
    ctx.fillRect(0, 0, width, height);
    // The recording shows a soft olive oval at the far end of the tube.
    const endScale = Math.min(width, height) * .93 / (depth * spacing + .8);
    ctx.save();
    ctx.translate(width * .56, height * .48);
    ctx.scale(4.6 * endScale, 3 * endScale);
    const haze = ctx.createRadialGradient(0, 0, .1, 0, 0, 1.7);
    haze.addColorStop(0, '#b4bd91');
    haze.addColorStop(.65, '#c6cdb0');
    haze.addColorStop(1, '#e5e7dc');
    ctx.fillStyle = haze;
    ctx.fillRect(-1.7, -1.7, 3.4, 3.4);
    ctx.restore();
    // Fixed world-space rings approach a fixed camera at constant velocity.
    // Neither the projection nor the clock depends on document scroll position.
    const travel = elapsed * speed, phase = travel % spacing;
    let far = ring(depth * spacing - phase);
    for (let j = depth-1; j >= 0; j--) {
      const z = j * spacing - phase;
      if (z < .15) continue;
      const near = ring(z);
      for (let i = 0; i < sides; i++) {
        const k = (i+1) % sides;
        const points = [near[i], near[k], far[k], far[i]];
        if (points.every(p => p[0] < 0) || points.every(p => p[0] > width) ||
            points.every(p => p[1] < 0) || points.every(p => p[1] > height)) continue;
        const band = (j + Math.floor(travel/spacing)) % 4 === 0 ? -1.6 : 0;
        const light = 85 + Math.cos(i * Math.PI * 2 / sides - .6) * 3 + z/(depth*spacing) * 3 + band;
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
    // Integrate every elapsed millisecond, even when a render frame is skipped.
    // Capping draw frequency must not change the flight speed.
    if (previous !== null) elapsed += (stamp-previous)/1000;
    previous = stamp;
    if (stamp-lastDraw >= 1000/30) {
      lastDraw = stamp;
      draw();
    }
    request = requestAnimationFrame(frame);
  }

  function sync() {
    cancelAnimationFrame(request);
    previous = null;
    lastDraw = 0;
    canvas.dataset.motion = paused ? 'paused' : 'running';
    if (toggle) {
      toggle.hidden = false;
      toggle.textContent = paused ? 'Play background' : 'Pause background';
      toggle.setAttribute('aria-pressed', String(paused));
    }
    if (!paused && !document.hidden) request = requestAnimationFrame(frame);
  }

  function resize() {
    // The canvas uses the large viewport height, which stays stable while
    // mobile browser toolbars expand/collapse during scrolling.
    const nextWidth = canvas.clientWidth, nextHeight = canvas.clientHeight;
    const nextRatio = Math.min(window.devicePixelRatio || 1, 1.5);
    if (nextWidth === width && nextHeight === height && nextRatio === ratio) return;
    width = nextWidth;
    height = nextHeight;
    ratio = nextRatio;
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
