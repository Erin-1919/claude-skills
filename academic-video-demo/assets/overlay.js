// Recording-time init script for a live app (passed to recorder.mjs start({ overlay })); the app's files stay unchanged.
// 1. Counts GET fetches in flight (window.__inflight), so the recorder captures a frame only once its data has arrived.
// 2. Adds a caption bar, a panel highlight with a dimmed surround, and a drawn cursor with a click ripple, driven by
//    window.__overlay. Sizes are in vw, so captions keep their size in the frame whatever the layout width.
//    Fades run on requestAnimationFrame, which the recorder's virtual clock steps frame by frame.
// Match the colours and font to the intro's theme. To reach an app object (a map, a chart), wrap its constructor here,
// e.g. intercept `window.mapboxgl` with Object.defineProperty and subclass Map to keep the instance on window.
(() => {
  window.__inflight = 0;
  const origFetch = window.fetch;
  window.fetch = (input, init) => {
    const get = !init || !init.method || init.method.toUpperCase() === "GET";
    if (!get) return origFetch(input, init);
    window.__inflight++;
    return origFetch(input, init).finally(() => { window.__inflight--; });
  };

  const CSS = `
  #__cap { position: fixed; left: 50%; bottom: 6.7vw; transform: translateX(-50%); width: max-content; max-width: 84vw; z-index: 2147483000;
    padding: .94vw 1.67vw 1.04vw 1.4vw; border-left: .31vw solid #0d9488; background: rgba(15,27,42,.93); color: #f4f7fa;
    font: 600 2.3vw/1.22 "IBM Plex Sans", system-ui, sans-serif; box-shadow: 0 8px 26px rgba(0,0,0,.4);
    opacity: 0; pointer-events: none; white-space: normal; text-align: left; }
  #__hl { position: fixed; z-index: 2147482000; border-radius: 6px; pointer-events: none; opacity: 0;
    outline: 4px solid #2dd4bf; outline-offset: 3px; box-shadow: 0 0 0 9999px rgba(15,27,42,.48); }
  #__cur { position: fixed; left: 0; top: 0; width: 29px; height: 38px; z-index: 2147483600; pointer-events: none;
    transform: translate(-100px, -100px); filter: drop-shadow(0 2px 3px rgba(0,0,0,.45)); }
  .__ripple { position: fixed; width: 22px; height: 22px; margin: -11px 0 0 -11px; border-radius: 50%; z-index: 2147483500;
    border: 3px solid #2dd4bf; pointer-events: none; }
  * { cursor: none !important; }`;
  // width: max-content matters: with left: 50% a fixed box otherwise shrinks to 50vw and wraps early

  const tween = (ms, f, done) => {
    const t0 = performance.now();
    const step = () => { const k = Math.min(1, (performance.now() - t0) / ms); f(k); if (k < 1) requestAnimationFrame(step); else if (done) done(); };
    requestAnimationFrame(step);
  };

  function mount() {
    const st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
    const cap = document.createElement("div"); cap.id = "__cap"; document.body.appendChild(cap);
    const hl = document.createElement("div"); hl.id = "__hl"; document.body.appendChild(hl);
    const cur = document.createElement("div"); cur.id = "__cur";
    cur.innerHTML = '<svg viewBox="0 0 26 34" width="29" height="38"><path d="M2 2 L2 27 L8.5 21 L13 31.5 L17.5 29.5 L13 19.5 L22 19.5 Z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg>';
    document.body.appendChild(cur);
    addEventListener("mousemove", (e) => { cur.style.transform = `translate(${e.clientX - 2}px, ${e.clientY - 2}px)`; }, true);
    addEventListener("mousedown", (e) => {
      const r = document.createElement("div"); r.className = "__ripple";
      r.style.left = `${e.clientX}px`; r.style.top = `${e.clientY}px`; document.body.appendChild(r);
      tween(550, (k) => { r.style.transform = `scale(${0.4 + 2.2 * k})`; r.style.opacity = String(1 - k); }, () => r.remove());
    }, true);

    const fade = (el, to, ms = 380, done) => { const from = Number(el.style.opacity || 0); tween(ms, (k) => { el.style.opacity = String(from + (to - from) * k); }, done); };
    let capText = null, track = null;
    window.__overlay = {
      // pos: a CSS bottom offset such as "6.7vw" (default) to keep the caption clear of a panel or timeline
      caption(text, pos = "6.7vw") {
        if (!text) { capText = null; fade(cap, 0); return; }
        if (capText === text) return;
        const show = () => { cap.textContent = text; cap.style.bottom = pos; fade(cap, 1); };
        if (capText) fade(cap, 0, 300, show); else show();
        capText = text;
      },
      highlight(selector) {
        if (track) cancelAnimationFrame(track);
        if (!selector) { fade(hl, 0); return; }
        const follow = () => {
          const el = document.querySelector(selector);
          if (el) {
            const r = el.getBoundingClientRect();
            Object.assign(hl.style, { left: `${r.left}px`, top: `${r.top}px`, width: `${r.width}px`, height: `${r.height}px` });
          }
          track = requestAnimationFrame(follow);
        };
        follow(); fade(hl, 1);
      },
    };
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
})();
