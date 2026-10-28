# Recording a live app off screen

Read this before writing the demo recorder (`scripts/recorder.mjs` is the core). It covers the patterns that made the GridMind booth recording deterministic, and the traps that cost a re-render each.

## Contents
- Clock and frames
- Waiting for content
- Canvases and maps
- Layout and framing
- Segments and stills
- Live model calls (chats)
- Toolchain traps

## Clock and frames

- `page.clock.install()` then `pauseAt()`: the page's timers and `requestAnimationFrame` advance only when `frame()` calls `clock.runFor(1000/30)`. App animations, map flights, and overlay fades are then frame-exact.
- Drive the app through its own UI or its exposed objects, one `frame()` per step. A camera move is `map.flyTo(...)` followed by `wait(seconds)`.
- Setup (loading data, choosing a tab, positioning the camera) runs before the first `segment()`, so it is never in the video.
- Mouse: move along an eased path one step per frame (`moveTo`), and draw a cursor in the overlay; headless Chrome draws none.

## Waiting for content

- Capture a frame only when its data has arrived: count fetches in flight in the init script (`window.__inflight`) and check the app's own readiness (for Mapbox, `map.areTilesLoaded()`). Waiting costs real time, never video time.
- `until(fn)` runs the clock without capture until a page condition holds: the right way to wait for a server answer without a frozen stretch in the video.

## Canvases and maps

- A WebGL map clears its canvas when its container resizes (panel opens, full screen toggles) and repaints only on its own resize: one white or black frame. Before each capture, compare the canvas size with `container size × devicePixelRatio`; if they differ, call `map.resize()` and `map._render(performance.now())`.
- Tiles that arrive after the frame's animation step are drawn only on the next step: after waiting, force a render without advancing the clock (`map._render(performance.now())`).
- Reach the app's map or chart object without editing the app: wrap the library constructor in the init script (`Object.defineProperty(window, "mapboxgl", { set(v) { subclass v.Map, keep the instance on window } })`).
- Run the flash scan (`scripts/flashscan.mjs`) on every rendered segment.

## Layout and framing

- Lay the app out at the size it is designed for (1440×810 for a laptop UI) and scale to 4K with `deviceScaleFactor` (8/3). Text keeps the size users know; a 1920 layout makes UI text too small.
- Use the app's default layers and settings; switch extra layers on for their shot only, on screen, and off afterwards.
- Full screen for the walkthrough, then the full layout once to show the panels (highlight each in turn), then interaction (chats).
- Popups and panels: before recording, measure every popup or panel you will open against the space it opens into. If it does not fit, pick another example or skip that interaction; do not let a panel cover it.

## Segments and stills

- Split each recording into segments at natural cuts (tour, chats). `--seg chats` re-renders one segment while the others run without capture, so a fix costs one segment. Plan segment boundaries before the first render.
- A cut must fall on a static frame (for example after a fade to no caption), so the hard cut between segments is invisible. Check the frames either side of every cut.
- `--stills <dir>` saves a still per shot and per popup; read all of them before showing the user.

## Live model calls (chats)

- Chat answers are real model calls: the recorder waits off camera (`until` without capture), then reveals the answer. Keep questions that answer from the agent's own records; check each answer for facts before keeping the take.
- Fix the content (run, agent, time point) in a targets file built by a script that queries the app's data, so every shot is reproducible and checked.

## Toolchain traps

- ffmpeg 9 removed `-vsync`; use `-fps_mode passthrough`.
- On Windows, quote filter expressions with commas: `select='between(n,10,20)'`; backslash-escaped commas fail under `spawn`.
- `conda run` breaks on multi-line `-c` scripts; write the script to a file. Call an env's `python.exe` directly when `conda run` swallows output.
- A server started for recording keeps running in the background: stop it when rendering ends.
