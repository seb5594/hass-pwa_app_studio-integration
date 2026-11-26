/* Home Assistant exposes card helpers when its Lovelace module has loaded. */
export async function loadPwaCardHelpers(hass) {
  if (!window.loadCardHelpers) {
    const main = document.querySelector("home-assistant")?.shadowRoot?.querySelector("home-assistant-main");
    const resolver = main?.shadowRoot?.querySelector("partial-panel-resolver");
    const routes = resolver?.routerOptions?.routes;
    const dashboard = Object.values(hass.panels || {}).find(panel => panel.component_name === "lovelace");
    await routes?.[dashboard?.url_path || "lovelace"]?.load?.();
  }
  if (!window.loadCardHelpers) {
    throw new Error("Dashboard-Karten konnten nicht geladen werden.");
  }
  return window.loadCardHelpers();
}
