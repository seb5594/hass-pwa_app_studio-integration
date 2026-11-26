/* Hidden native HA panel rendering authorized PWAs inside the HA context-request tree. */

class PwaAppStudioRunnerPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._appSlug = null;
    this._runtimeData = null;
    this._dashboardViews = [];
    this._activeViewIdx = 0;
    this._error = null;
    this._renderedElements = [];
    this._loading = true;
  }

  _esc(val) {
    return String(val ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  set hass(value) {
    const firstInit = !this._hass && value;
    this._hass = value;
    for (const el of this._renderedElements) {
      try {
        el.hass = value;
      } catch (_e) {
        // Ignore transient setter failures
      }
    }
    if (firstInit) {
      if (!this._appSlug) {
        this._appSlug = new URLSearchParams(window.location.search).get("app") || "";
      }
      this._bootstrap();
    }
  }

  set route(value) {
    const pathPart = (value?.path || "").replace(/^\/+/, "").split("/")[0];
    const querySlug = new URLSearchParams(window.location.search).get("app");
    const nextSlug = querySlug || pathPart || "";
    if (nextSlug && nextSlug !== this._appSlug) {
      this._appSlug = nextSlug;
      if (this._hass) this._bootstrap();
    }
  }

  connectedCallback() {
    const querySlug = new URLSearchParams(window.location.search).get("app");
    if (querySlug) this._appSlug = querySlug;
    this._renderShell();
  }

  async _bootstrap() {
    if (!this._hass || !this._appSlug) return;
    this._loading = true;
    this._error = null;
    this._renderShell();

    try {
      const data = await this._hass.callWS({
        type: "pwa_app_studio/runtime/get",
        slug: this._appSlug,
      });
      this._runtimeData = data;

      if (data.content.source_mode === "lovelace_dashboard") {
        const urlPath =
          data.content.dashboard_url_path === "lovelace"
            ? null
            : data.content.dashboard_url_path;
        const lovelaceConfig = await this._hass.callWS({
          type: "lovelace/config",
          url_path: urlPath,
        });
        const views = Array.isArray(lovelaceConfig?.views) ? lovelaceConfig.views : [];
        this._dashboardViews = views;
        if (data.content.view_path) {
          const idx = views.findIndex(
            (v, i) => String(v.path ?? i) === String(data.content.view_path)
          );
          this._activeViewIdx = idx >= 0 ? idx : 0;
        }
      }
      this._loading = false;
      this._renderShell();
      await this._mountCards();
    } catch (err) {
      this._loading = false;
      this._error = err?.message || "Zugriff verweigert oder Dashboard nicht ladbar.";
      this._renderShell();
    }
  }

  _extractViewCards(view) {
    if (!view) return [];
    const items = [];
    if (Array.isArray(view.cards)) {
      for (const cfg of view.cards) items.push({ config: cfg, col_span: 1 });
    }
    if (Array.isArray(view.sections)) {
      for (const sec of view.sections) {
        if (Array.isArray(sec?.cards)) {
          for (const cfg of sec.cards) items.push({ config: cfg, col_span: sec.column_span || 1 });
        }
      }
    }
    return items;
  }

  async _mountCards() {
    const container = this.shadowRoot.getElementById("cards-stage");
    if (!container || !this._runtimeData || !this._hass) return;
    container.innerHTML = "";
    this._renderedElements = [];

    if (!window.loadCardHelpers) {
      container.innerHTML = `<div class="msg">Home Assistant Card Helpers werden geladen...</div>`;
      return;
    }

    const helpers = await window.loadCardHelpers();
    const content = this._runtimeData.content;

    let cardItems = [];
    if (content.source_mode === "lovelace_dashboard") {
      const view = this._dashboardViews[this._activeViewIdx];
      cardItems = this._extractViewCards(view);
    } else {
      cardItems = Array.isArray(content.cards) ? content.cards : [];
    }

    if (!cardItems.length) {
      container.innerHTML = `<div class="msg">Keine Karten konfiguriert.</div>`;
      return;
    }

    for (const item of cardItems) {
      const slot = document.createElement("div");
      slot.className = "card-slot";
      slot.style.gridColumn = `span ${Math.min(content.grid_columns || 2, item.col_span || 1)}`;
      try {
        const el = helpers.createCardElement(item.config);
        el.hass = this._hass;
        slot.appendChild(el);
        this._renderedElements.push(el);
      } catch (err) {
        slot.innerHTML = `<div class="err-card">Kartenfehler: ${this._esc(err?.message || err)}</div>`;
      }
      container.appendChild(slot);
    }
  }

  _renderShell() {
    const manifest = this._runtimeData?.manifest || {};
    const content = this._runtimeData?.content || {};
    const showHeader = !manifest.kiosk_mode && !manifest.hide_ha_header;
    const cols = content.layout_mode === "stack" ? 1 : content.grid_columns || 2;
    const showViewTabs =
      content.source_mode === "lovelace_dashboard" &&
      !content.view_path &&
      this._dashboardViews.length > 1;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          min-height: 100vh;
          background: var(--primary-background-color, #111827);
          color: var(--primary-text-color, #f8fafc);
          font-family: var(--paper-font-body1_-_font-family, system-ui, sans-serif);
          padding-bottom: env(safe-area-inset-bottom, 12px);
        }
        header {
          display: ${showHeader ? "flex" : "none"};
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          background: ${this._esc(manifest.theme_color || "var(--app-header-background-color, #03a9f4)")};
          color: #ffffff;
          position: sticky;
          top: 0;
          z-index: 10;
        }
        header h1 {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
        }
        .tabs {
          display: ${showViewTabs ? "flex" : "none"};
          gap: 8px;
          padding: 10px 14px 0;
          overflow-x: auto;
        }
        .tab-btn {
          border: 1px solid var(--divider-color, rgba(255,255,255,0.16));
          background: var(--card-background-color, #1e293b);
          color: var(--primary-text-color, #f8fafc);
          padding: 6px 14px;
          border-radius: 999px;
          cursor: pointer;
          font-size: 13px;
          white-space: nowrap;
        }
        .tab-btn.active {
          background: var(--primary-color, #03a9f4);
          color: #ffffff;
          border-color: transparent;
        }
        #cards-stage {
          display: grid;
          grid-template-columns: repeat(${cols}, minmax(0, 1fr));
          gap: 12px;
          padding: 14px;
          align-items: start;
        }
        @media (max-width: 680px) {
          #cards-stage {
            grid-template-columns: minmax(0, 1fr);
          }
          .card-slot {
            grid-column: span 1 !important;
          }
        }
        .msg, .err-card {
          background: var(--card-background-color, #1e293b);
          border: 1px solid var(--divider-color, rgba(255,255,255,0.12));
          border-radius: 12px;
          padding: 16px;
        }
        .err-card {
          color: #fca5a5;
          border-color: #ef4444;
        }
      </style>
      <header>
        <h1>${this._esc(manifest.name || "Home Assistant PWA")}</h1>
        <span style="font-size:12px;opacity:0.9">${this._esc(this._runtimeData?.user?.name || "")}</span>
      </header>
      <div class="tabs" id="view-tabs">
        ${this._dashboardViews
          .map(
            (v, idx) => `
          <button class="tab-btn ${idx === this._activeViewIdx ? "active" : ""}" data-idx="${idx}">
            ${this._esc(v.title || v.path || `View ${idx + 1}`)}
          </button>`
          )
          .join("")}
      </div>
      ${
        this._loading
          ? `<div style="padding:16px"><div class="msg">Lade PWA-Ansicht...</div></div>`
          : this._error
          ? `<div style="padding:16px"><div class="err-card">${this._esc(this._error)}</div></div>`
          : `<div id="cards-stage"></div>`
      }
    `;

    this.shadowRoot.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        this._activeViewIdx = Number(btn.dataset.idx || 0);
        this._renderShell();
        this._mountCards();
      });
    });
  }
}

if (!customElements.get("pwa-app-studio-runner-panel")) {
  customElements.define("pwa-app-studio-runner-panel", PwaAppStudioRunnerPanel);
}
