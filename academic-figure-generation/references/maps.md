# Maps

## Study-area map essentials

- Base map with place names for orientation; locator inset showing the study area in its region; scale bar; legend; units where a value is mapped.
- Show the objects the text names. If the text identifies cells, tiles, or zones by ID, label them on the map so the text can cite them ("N64824 and N64827").
- Keep overlays the user did not ask for off the map. Nested study regions can be named in the text from labelled cells instead of drawn as extra outlines.
- Match a project UI style when the paper describes a system with one (same base map, grid color, icons), so the map and screenshots of the system read as one.
- Caption: one sentence; country in the place name.

## Fast route: HTML map → screenshot

Often quicker than ArcGIS or QGIS when the user only needs an image.

1. A data script writes the layers as GeoJSON (EPSG:4326) into a gitignored `figN_data/` folder, asserting the counts the text reports.
2. A page script writes one self-contained HTML file: layers inlined as JSON, icons as data URIs, the map token read from the project `.env` (the output stays gitignored because it embeds the token).
3. The user opens it, frames it, and screenshots it as `figureN.png`.

Mapbox GL / MapLibre specifics:

- Add sources and layers in `map.on("style.load", …)`. Layers added on `load` did not render reliably, especially headless.
- Insert data layers below the first symbol layer (`map.getStyle().layers.find(l => l.type === "symbol").id`) so place names stay on top; add ID labels last so they sit above everything.
- Enlarge base-map place names (`setLayoutProperty(id, "text-size", 20)`, white text with a black halo) and the scale bar and legend (22 px) for print.
- Distinguish grid levels by line width and opacity in one color, not by different hues.
- Leave fitBounds padding on the side where the inset sits so it does not cover the study area.
- Headless preview: Chrome `--headless --screenshot --window-size=1600,1200 --virtual-time-budget=15000`; tiles and glyphs load slowly, so raise the budget if layers are missing. Look at the result before handing it over.

## Scripted maps (matplotlib / geopandas)

- Use them when the map shows computed values that must stay reproducible (choropleth of results, error map).
- Classification: state method and class count; avoid breaks that manufacture clusters; sequential ramp for magnitude, diverging only around a meaningful midpoint.
- Same fonts and palette as the other figures.
