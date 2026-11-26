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
    let subscribed = false;

    const trySubscribe = () => {
      if (subscribed) return;
      const ha = document.querySelector("home-assistant");
      const hass = ha?.hass;
      if (!hass?.connection || !hass?.user) return;

      if (!hass.user.is_admin) {
        subscribed = true;
        return;
      }

      subscribed = true;
      hass.connection.subscribeEvents((event) => {
        const currentHass = document.querySelector("home-assistant")?.hass;
        if (!currentHass?.user?.is_admin) return;
        const target = event?.data?.panel_path || "/pwa-app-studio";
        if (window.location.pathname !== target) {
          window.history.pushState(null, "", target);
          window.dispatchEvent(new CustomEvent("location-changed"));
        }
      }, EVENT_NAME);
    };

    const timer = setInterval(() => {
      trySubscribe();
      if (subscribed) clearInterval(timer);
    }, 800);
    trySubscribe();
  }

  applyEmbeddedPwaChromeHiding();
  initAdminEventBridge();
})();
