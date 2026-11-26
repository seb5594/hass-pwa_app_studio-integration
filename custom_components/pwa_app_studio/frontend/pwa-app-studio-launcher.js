/* Global launcher hook: handles admin ButtonEntity navigation and embedded PWA shell chrome hiding. */

(() => {
  const EVENT_NAME = "pwa_app_studio_open_designer";

  function applyEmbeddedPwaChromeHiding() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("pwa_shell") !== "1") return;
    if (document.getElementById("pwa-app-studio-shell-style")) return;

    const style = document.createElement("style");
    style.id = "pwa-app-studio-shell-style";
    style.textContent = `
      home-assistant {
        --mdc-drawer-width: 0px !important;
      }
    `;
    document.head.appendChild(style);

    const hideDrawer = () => {
      try {
        const ha = document.querySelector("home-assistant");
        const main = ha?.shadowRoot?.querySelector("home-assistant-main");
        const drawer = main?.shadowRoot?.querySelector("ha-drawer");
        const aside = drawer?.shadowRoot?.querySelector(".mdc-drawer");
        if (aside) aside.style.display = "none";
        const appContent = drawer?.shadowRoot?.querySelector(".mdc-drawer-app-content");
        if (appContent) {
          appContent.style.marginLeft = "0px";
          appContent.style.width = "100%";
        }
      } catch (_err) {
        // Ignore shadow boundary timing errors
      }
    };
    setInterval(hideDrawer, 400);
    hideDrawer();
  }

  function initAdminEventBridge() {
    let connection;
    let unsubscribe;
    async function subscribe() {
      const hass = document.querySelector("home-assistant")?.hass;
      if (!hass?.user?.is_admin || !hass.connection || connection === hass.connection) return;
      unsubscribe?.();
      unsubscribe = undefined;
      const active = connection = hass.connection;
      try {
        const stop = await active.subscribeEvents(({ data }) => {
          if (connection !== active || document.visibilityState !== "visible") return;
          if (data.triggered_by !== hass.user.id) return;
          window.location.assign("/pwa-app-studio");
        }, EVENT_NAME);
        if (connection === active) unsubscribe = stop;
        else stop();
      } catch {
        if (connection === active) connection = undefined;
      }
    }
    subscribe();
    window.addEventListener("pageshow", subscribe);
    document.addEventListener("visibilitychange", subscribe);
    setInterval(subscribe, 1500);
  }

  applyEmbeddedPwaChromeHiding();
  initAdminEventBridge();
})();
