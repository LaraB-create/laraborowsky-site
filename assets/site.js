// laraborowsky.com — reading settings, theme and depth.
// Settings live in this browser only (localStorage). Nothing is sent anywhere.
(function () {
  var KEY = 'lb-settings';
  var DEFAULTS = { theme: 'auto', font: 'default', size: 'standard', spacing: 'standard', motion: 'auto', depth: 'tldr' };
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function load() {
    var s = {};
    try { s = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { s = {}; }
    var out = {};
    for (var k in DEFAULTS) out[k] = s[k] || DEFAULTS[k];
    return out;
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  var state = load();

  function apply() {
    var dark = state.theme === 'dark' || (state.theme === 'auto' && media && media.matches);
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    root.setAttribute('data-font', state.font);
    root.setAttribute('data-size', state.size);
    root.setAttribute('data-spacing', state.spacing);
    if (state.motion === 'auto') root.removeAttribute('data-motion'); else root.setAttribute('data-motion', state.motion);
    root.setAttribute('data-depth', state.depth);

    var btns = document.querySelectorAll('[data-set]');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      b.setAttribute('aria-pressed', String(state[b.getAttribute('data-set')] === b.getAttribute('data-val')));
    }
    var tb = document.querySelectorAll('.theme-btn');
    for (var j = 0; j < tb.length; j++) {
      var label = dark ? 'Switch to light mode' : 'Switch to dark mode';
      tb[j].setAttribute('aria-label', label);
      tb[j].setAttribute('title', label);
    }
  }

  function set(key, val) { state[key] = val; save(state); apply(); }

  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-set],[data-action]') : null;
    if (!t) return;
    if (t.hasAttribute('data-set')) {
      set(t.getAttribute('data-set'), t.getAttribute('data-val'));
      return;
    }
    var action = t.getAttribute('data-action');
    if (action === 'toggle-theme') {
      set('theme', root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    } else if (action === 'toggle-settings') {
      var panel = document.getElementById('reading-settings');
      var open = panel.hasAttribute('hidden');
      if (open) panel.removeAttribute('hidden'); else panel.setAttribute('hidden', '');
      t.setAttribute('aria-expanded', String(open));
      if (open) { var first = panel.querySelector('button'); if (first) first.focus(); }
    } else if (action === 'reset-settings') {
      state = Object.assign({}, DEFAULTS); save(state); apply();
    }
  });

  if (media) {
    var onChange = function () { if (state.theme === 'auto') apply(); };
    if (media.addEventListener) media.addEventListener('change', onChange); else if (media.addListener) media.addListener(onChange);
  }

  var y = document.querySelectorAll('[data-year]');
  for (var n = 0; n < y.length; n++) y[n].textContent = new Date().getFullYear();

  apply();
})();
