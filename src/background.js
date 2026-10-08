// The tunnel is drawn and animated entirely in CSS. JS only manages preferences.
(() => {
  'use strict';
  const tunnel = document.getElementById('electrosphere');
  const toggle = document.getElementById('motion');
  if (!tunnel) return;
  const preference = window.matchMedia?.('(prefers-reduced-motion: reduce)');
  const storageKey = 'ac3-jp-background-motion';
  let paused = preference?.matches || false;
  try { paused ||= localStorage.getItem(storageKey) === 'paused'; } catch (_) {}

  function sync() {
    tunnel.dataset.motion = paused ? 'paused' : 'running';
    tunnel.dataset.hidden = String(document.hidden);
    if (toggle) {
      toggle.hidden = false;
      toggle.textContent = paused ? 'Play background' : 'Pause background';
      toggle.setAttribute('aria-pressed', String(paused));
    }
  }

  toggle?.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem(storageKey, paused ? 'paused' : 'running'); } catch (_) {}
    sync();
  });
  preference?.addEventListener('change', event => { paused = event.matches; sync(); });
  document.addEventListener('visibilitychange', sync);
  sync();
})();
