/* Admin-only PWA Web-App Studio Designer custom panel with Live Device Preview, Multi-Card Composer, Icon Studio & QR Distribution. */

import { loadPwaCardHelpers } from "./pwa-card-helpers.js";

const STUDIO_ACCENT = "#2563eb";
const STUDIO_LOGO = new URL("./studio-logo.png", import.meta.url).href;

const STEPS = [
  { id: "general", label: "App", icon: "creation-outline", title: "Wie heißt deine App?", hint: "Wähle einen Namen, eine Farbe und den ersten Eindruck beim Öffnen." },
  { id: "content", label: "Inhalt", icon: "view-dashboard-outline", title: "Was soll deine App zeigen?", hint: "Übernimm ein Dashboard oder stelle einzelne Karten zusammen." },
  { id: "icon", label: "Symbol", icon: "shape-outline", title: "Woran erkennst du deine App?", hint: "Dieses Symbol erscheint auf dem Startbildschirm." },
  { id: "access", label: "Zugriff", icon: "account-key-outline", title: "Wer darf die App öffnen?", hint: "Wähle die Personen aus, für die deine App gedacht ist." },
  { id: "distribute", label: "Teilen", icon: "qrcode-scan", title: "Wie kommt die App aufs Handy?", hint: "Speichere deine Auswahl und öffne die App oder teile den QR-Code." },
];

const CARD_PRESETS = {
  tile: {
    label: "Tile-Karte",
    config: { type: "tile", entity: "sun.sun", name: "Beispiel Tile" },
  },
  markdown: {
    label: "Markdown-Text",
    config: {
      type: "markdown",
      title: "Status",
      content: "## Willkommen\nSonnenstand: **{{ states('sun.sun') }}**",
    },
  },
  entities: {
    label: "Entitäten-Liste",
    config: {
      type: "entities",
      title: "Geräte",
      entities: ["sun.sun"],
    },
  },
  gauge: {
    label: "Gauge / Pegel",
    config: {
      type: "gauge",
      entity: "sensor.sun_next_dawn",
      name: "Messwert",
      min: 0,
      max: 100,
    },
  },
  weather: {
    label: "Wetter-Karte",
    config: {
      type: "weather-forecast",
      entity: "weather.forecast_home",
    },
  },
};

const DEVICE_DIMENSIONS = {
  desktop: { label: "Computer", width: 1280, height: 800, scale: 0.46 },
  tablet: { label: "Tablet", width: 768, height: 1024, scale: 0.56 },
  smartphone: { label: "Smartphone", width: 390, height: 844, scale: 0.68 },
};

class PwaAppStudioPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._panel = null;
    this._apps = [];
    this._dashboards = [];
    this._users = [];
    this._selectedAppId = null;
    this._draft = null;
    this._activeTab = "general";
    this._previewDevice = "smartphone";
    this._mobilePane = "editor";
    this._previewRotated = false;
    this._iconPreviewUrl = null;
    this._qrInfo = null;
    this._statusMsg = "";
    this._errorMsg = "";
    this._dragCardIndex = null;
    this._previewCardElements = [];
    this._initialized = false;
  }

  disconnectedCallback() {
    this._previewObserver?.disconnect();
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
    const isFirst = !this._hass && value;
    this._hass = value;
    for (const el of this._previewCardElements) {
      try {
        el.hass = value;
      } catch (_e) {
        // Ignore transient updates
      }
    }
    if (isFirst) {
      this._bootstrap();
    }
  }

  set panel(value) {
    this._panel = value;
  }

  connectedCallback() {
    const wrap = this.shadowRoot.querySelector(".device-bezel-wrap");
    if (wrap) this._previewObserver?.observe(wrap);
    if (!this._initialized) {
      this._render();
      this._initialized = true;
    }
  }

  _detectCurrentDevice() {
    const uaData = navigator.userAgentData;
    const ua = navigator.userAgent || "";
    const platform = uaData?.platform || navigator.platform || "";
    const isTouchMac = /Mac/i.test(platform) && navigator.maxTouchPoints > 1;
    const isIos = /iPhone|iPad|iPod/i.test(ua) || isTouchMac;
    const isAndroid = /Android/i.test(ua) || /Android/i.test(platform);
    const isTablet =
      isTouchMac ||
      /iPad|Tablet/i.test(ua) ||
      (isAndroid && !/Mobile/i.test(ua));
    const isEdge =
      Boolean(uaData?.brands?.some((b) => /Edge/i.test(b.brand))) || /Edg/i.test(ua);
    const hasNativePrompt = !isIos && "onbeforeinstallprompt" in window;

    let previewTarget = "desktop";
    let osLabel = `Computer (${platform || "Desktop"} / ${isEdge ? "Edge" : "Browser"})`;
    if (isIos) {
      previewTarget = isTablet ? "tablet" : "smartphone";
      osLabel = isTablet ? "iPadOS (Safari)" : "iOS (Safari)";
    } else if (isAndroid) {
      previewTarget = isTablet ? "tablet" : "smartphone";
      osLabel = isTablet ? "Android Tablet" : "Android Smartphone";
    }

    return {
      previewTarget,
      osLabel,
      hasNativePrompt,
      isIos,
      isStandalone:
        window.matchMedia?.("(display-mode: standalone)").matches ||
        window.navigator.standalone === true,
    };
  }

  async _bootstrap() {
    if (!this._hass) return;
    if (!this._hass.user?.is_admin) {
      this._errorMsg = "Zugriff nur für Home-Assistant-Administratoren.";
      this._render();
      return;
    }

    const detected = this._detectCurrentDevice();
    this._previewDevice = detected.previewTarget;

    try {
      const [appsRes, dashRes, usersRes] = await Promise.all([
        this._hass.callWS({ type: "pwa_app_studio/apps/list" }),
        this._hass.callWS({ type: "pwa_app_studio/lovelace/list" }),
        this._hass.callWS({ type: "pwa_app_studio/users/list" }),
      ]);
      this._apps = appsRes.apps || [];
      this._dashboards = dashRes.dashboards || [];
      this._users = usersRes.users || [];

      if (this._apps.length > 0) {
        this._selectApp(this._apps[0].app_id);
      } else {
        this._newAppDraft();
      }
    } catch (err) {
      this._errorMsg = err?.message || "Fehler beim Laden der PWA-App-Studio-Daten.";
      this._render();
    }
  }

  _createEmptyDraft() {
    const styles = getComputedStyle(this);
    const canvas = document.createElement("canvas").getContext("2d");
    function themeColor(names, fallback) {
      canvas.fillStyle = fallback;
      for (const name of names) {
        const value = styles.getPropertyValue(name).trim();
        if (value && CSS.supports("color", value)) {
          canvas.fillStyle = value;
          break;
        }
      }
      canvas.fillRect(0, 0, 1, 1);
      const rgb = canvas.getImageData(0, 0, 1, 1).data.slice(0, 3);
      return "#" + Array.from(rgb, n => n.toString(16).padStart(2, "0")).join("");
    }
    const firstDash = this._dashboards[0]?.url_path || "lovelace";
    return {
      app_id: null,
      slug: "",
      manifest: {
        name: "Smart Home App",
        short_name: "SmartHome",
        description: "Maßgeschneiderte Home Assistant PWA",
        display: "standalone",
        orientation: "any",
        theme_color: STUDIO_ACCENT,
        background_color: themeColor(["--primary-background-color"], "#111827"),
        lang: "de",
        dir: "ltr",
        categories: ["utilities"],
        shortcuts: [],
        prefer_related_applications: false,
        offline_enabled: true,
        cache_strategy: "network_first",
        hide_ha_header: true,
        hide_ha_sidebar: true,
        kiosk_mode: false,
      },
      content: {
        source_mode: "lovelace_dashboard",
        dashboard_url_path: firstDash,
        view_path: "",
        cards: [],
        layout_mode: "grid",
        grid_columns: 2,
        default_preview_device: this._previewDevice,
      },
      icon: {
        mode: "ha_default",
        mdi_icon: "mdi:home-assistant",
        icon_svg_path: "",
        icon_color: "#ffffff",
        bg_color: STUDIO_ACCENT,
        badge_icon: "mdi:lightbulb",
        badge_svg_path: "",
        badge_color: "#ffffff",
        badge_bg_color: "#111827",
        badge_position: "bottom_right",
        uploaded_image_b64: "",
        uploaded_mime: "image/png",
        corner_radius_pct: 22,
        maskable_padding_pct: 12,
        resolved_dashboard_icon: "",
      },
      access: {
        allow_all_authenticated: true,
        allowed_user_ids: [],
        require_admin: false,
      },
    };
  }

  _newAppDraft() {
    this._activeTab = "general";
    this._statusMsg = "";
    this._errorMsg = "";
    this._mobilePane = "editor";
    this._selectedAppId = null;
    this._draft = this._createEmptyDraft();
    this._qrInfo = null;
    this._render();
    this._refreshIconPreview();
    this._renderDevicePreviewCards();
  }

  _selectApp(appId) {
    this._mobilePane = "editor";
    const found = this._apps.find((a) => a.app_id === appId);
    if (!found) return;
    this._selectedAppId = found.app_id;
    this._draft = JSON.parse(JSON.stringify(found));
    this._previewDevice = this._draft.content?.default_preview_device || "smartphone";
    this._qrInfo = null;
    this._render();
    this._refreshIconPreview();
    this._renderDevicePreviewCards();
    if (this._activeTab === "distribute") {
      this._loadQrCode();
    }
  }

  async _extractMdiSvgPath(iconName) {
    if (!iconName || !iconName.includes(":")) return "";
    return new Promise((resolve) => {
      const host = document.createElement("div");
      host.style.cssText = "position:fixed;left:-9999px;top:-9999px;opacity:0;pointer-events:none;";
      const haIcon = document.createElement("ha-icon");
      haIcon.setAttribute("icon", iconName);
      host.appendChild(haIcon);
      this.shadowRoot.appendChild(host);

      let tries = 0;
      const poll = () => {
        tries += 1;
        const svgIcon = haIcon.shadowRoot?.querySelector("ha-svg-icon");
        const path =
          svgIcon?.shadowRoot?.querySelector("path")?.getAttribute("d") ||
          haIcon.shadowRoot?.querySelector("path")?.getAttribute("d") ||
          "";
        if (path || tries >= 12) {
          host.remove();
          resolve(path || "");
        } else {
          setTimeout(poll, 35);
        }
      };
      setTimeout(poll, 25);
    });
  }

  async _syncIconPathsBeforePreviewOrSave() {
    if (!this._draft) return;
    const icon = this._draft.icon;
    let mainIcon = icon.mdi_icon;
    if (icon.mode === "dashboard_default") {
      const dash = this._dashboards.find(
        (d) => d.url_path === this._draft.content.dashboard_url_path
      );
      mainIcon = dash?.icon || "mdi:view-dashboard";
      icon.resolved_dashboard_icon = mainIcon;
    }
    icon.icon_svg_path = await this._extractMdiSvgPath(mainIcon);
    icon.badge_svg_path = await this._extractMdiSvgPath(icon.badge_icon);
  }

  _updateSampleIcon(sample) {
    const mark = sample?.shadowRoot?.querySelector(".mark");
    if (!mark) return;
    let img = mark.querySelector("img");
    if (!img) {
      img = new Image(76, 76);
      img.alt = "";
      mark.replaceChildren(img);
    }
    img.src = this._iconPreviewUrl;
  }

  async _refreshIconPreview() {
    if (!this._hass || !this._draft) return;
    const requestId = this._iconRequestId = (this._iconRequestId || 0) + 1;
    await this._syncIconPathsBeforePreviewOrSave();
    try {
      const token = this._hass.auth?.data?.access_token;
      const resp = await fetch("/api/pwa_app_studio/icon_preview", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ icon: this._draft.icon, size: 192, maskable: false }),
      });
      if (!resp.ok) return;
      const blob = await resp.blob();
      if (requestId !== this._iconRequestId) return;
      if (this._iconPreviewUrl) URL.revokeObjectURL(this._iconPreviewUrl);
      this._iconPreviewUrl = URL.createObjectURL(blob);
      const img = this.shadowRoot.getElementById("live-icon-img");
      if (img) img.src = this._iconPreviewUrl;
      this._updateSampleIcon(this.shadowRoot.getElementById("launch-sample"));
    } catch (_e) {
      // Ignore preview errors
    }
  }

  async _saveApp() {
    if (!this._hass || !this._draft || this._saving) return;
    this._saving = true;
    const draft = this._draft;
    const selectedId = this._selectedAppId;
    this._statusMsg = "Speichere PWA...";
    this._errorMsg = "";
    this._render();

    try {
      await this._syncIconPathsBeforePreviewOrSave();
      let saved;
      if (selectedId) {
        const res = await this._hass.callWS({
          type: "pwa_app_studio/apps/update",
          app_id: selectedId,
          payload: draft,
        });
        saved = res.app;
      } else {
        const res = await this._hass.callWS({
          type: "pwa_app_studio/apps/create",
          payload: draft,
        });
        saved = res.app;
      }
      const appsRes = await this._hass.callWS({ type: "pwa_app_studio/apps/list" });
      this._apps = appsRes.apps || [];
      if (this._draft !== draft) return;
      this._statusMsg = `PWA '${saved.manifest.name}' gespeichert (v${saved.version}).`;
      this._selectApp(saved.app_id);
    } catch (err) {
      if (this._draft !== draft) return;
      this._errorMsg = err?.message || "Speichern fehlgeschlagen.";
      this._statusMsg = "";
      this._render();
    } finally {
      this._saving = false;
    }
  }

  async _deleteApp(appId) {
    if (!this._hass || !appId) return;
    if (!confirm("Diese PWA wirklich unwiderruflich löschen?")) return;
    try {
      await this._hass.callWS({ type: "pwa_app_studio/apps/delete", app_id: appId });
      const appsRes = await this._hass.callWS({ type: "pwa_app_studio/apps/list" });
      this._apps = appsRes.apps || [];
      this._statusMsg = "PWA gelöscht.";
      if (this._apps.length > 0) {
        this._selectApp(this._apps[0].app_id);
      } else {
        this._newAppDraft();
      }
    } catch (err) {
      this._errorMsg = err?.message || "Löschen fehlgeschlagen.";
      this._render();
    }
  }

  async _loadQrCode() {
    if (!this._hass || !this._selectedAppId) return;
    const appId = this._selectedAppId;
    try {
      const info = await this._hass.callWS({
        type: "pwa_app_studio/qr/generate",
        app_id: this._selectedAppId,
        origin: window.location.origin,
      });
      if (appId !== this._selectedAppId) return;
      this._qrInfo = info;
      this._render();
    } catch (err) {
      if (appId !== this._selectedAppId) return;
      this._qrInfo = null;
      this._errorMsg = err?.message || "QR-Code konnte nicht generiert werden.";
      this._render();
    }
  }

  async _renderDevicePreviewCards() {
    const stage = this.shadowRoot.getElementById("preview-stage");
    if (!stage || !this._hass || !this._draft) return;
    stage.innerHTML = "";
    this._previewCardElements = [];

    let helpers;
    try {
      helpers = await loadPwaCardHelpers(this._hass);
    } catch (err) {
      const message = document.createElement("div");
      message.className = "preview-empty";
      message.textContent = err?.message || "Die Kartenvorschau ist gerade nicht verfügbar.";
      stage.appendChild(message);
      return;
    }
    if (!stage.isConnected) return;
    const content = this._draft.content;
    let items = [];

    if (content.source_mode === "lovelace_dashboard") {
      const dash = this._dashboards.find(
        (d) => d.url_path === content.dashboard_url_path
      );
      const views = dash?.views || [];
      const view =
        (content.view_path
          ? views.find((v) => String(v.path) === String(content.view_path))
          : views[0]);
      items = (view?.cards || []).map((cfg, idx) => ({
        id: `dash-${idx}`,
        col_span: 1,
        config: cfg,
      }));
    } else {
      items = content.cards || [];
    }

    if (!items.length) {
      stage.innerHTML = `<div class="preview-empty">Keine Karten in dieser Auswahl. Füge Karten im Tab "Inhalt & Karten" hinzu.</div>`;
      return;
    }

    const cols =
      this._previewDevice === "smartphone" || content.layout_mode === "stack"
        ? 1
        : content.grid_columns || 2;
    stage.style.gridTemplateColumns = `repeat(${cols}, minmax(0, 1fr))`;

    for (const item of items) {
      const wrap = document.createElement("div");
      wrap.className = "preview-card-wrap";
      wrap.style.gridColumn = `span ${Math.min(cols, item.col_span || 1)}`;
      try {
        const el = helpers.createCardElement(item.config);
        el.hass = this._hass;
        wrap.appendChild(el);
        this._previewCardElements.push(el);
      } catch (err) {
        wrap.innerHTML = `<div class="preview-err">Kartenfehler (${this._esc(item.config?.type || "?")}): ${this._esc(err?.message || err)}</div>`;
      }
      stage.appendChild(wrap);
    }
  }

  _reorderCard(fromIdx, toIdx) {
    const cards = this._draft.content.cards;
    if (toIdx < 0 || toIdx >= cards.length) return;
    const [moved] = cards.splice(fromIdx, 1);
    cards.splice(toIdx, 0, moved);
    cards.forEach((c, idx) => {
      c.order = idx;
    });
    this._render();
    this._renderDevicePreviewCards();
  }

  _cardPresets() {
    const [year, month] = (this._hass?.config?.version || "").split(".").map(Number);
    if (year === 2021 || (year === 2022 && month < 11)) {
      return {
        ...CARD_PRESETS,
        tile: { label: "Schaltfläche", config: { type: "button", entity: "sun.sun", name: "Sonnenstand" } },
      };
    }
    return CARD_PRESETS;
  }

  _addPresetCard(presetKey) {
    const preset = this._cardPresets()[presetKey];
    if (!preset) return;
    this._draft.content.source_mode = "lovelace_cards";
    this._draft.content.cards.push({
      id: `card-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
      order: this._draft.content.cards.length,
      title: preset.label,
      col_span: 1,
      config: JSON.parse(JSON.stringify(preset.config)),
    });
    this._render();
    this._renderDevicePreviewCards();
  }

  _importCardFromDashboard(cardConfig) {
    this._draft.content.source_mode = "lovelace_cards";
    this._draft.content.cards.push({
      id: `card-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
      order: this._draft.content.cards.length,
      title: cardConfig.title || cardConfig.name || cardConfig.type || "Importierte Karte",
      col_span: 1,
      config: JSON.parse(JSON.stringify(cardConfig)),
    });
    this._render();
    this._renderDevicePreviewCards();
  }

  _importWholeDashboardViewAsCards() {
    const dash = this._dashboards.find(
      (db) => db.url_path === this._draft.content.dashboard_url_path
    );
    const views = dash?.views || [];
    const view =
      (this._draft.content.view_path
        ? views.find((v) => String(v.path) === String(this._draft.content.view_path))
        : views[0]);
    const cards = view?.cards || [];
    if (!cards.length) {
      this._errorMsg = "Die ausgewählte View enthält keine direkt importierbaren Karten.";
      this._render();
      return;
    }
    this._draft.content.source_mode = "lovelace_cards";
    for (const cfg of cards) {
      this._draft.content.cards.push({
        id: `card-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
        order: this._draft.content.cards.length,
        title: cfg.title || cfg.name || cfg.type || "Dashboard-Karte",
        col_span: 1,
        config: JSON.parse(JSON.stringify(cfg)),
      });
    }
    this._statusMsg = `${cards.length} Karte(n) aus '${dash.title}' in den Karten-Composer übernommen.`;
    this._render();
    this._renderDevicePreviewCards();
  }

  _handleInstallOnCurrentDevice() {
    if (!this._selectedAppId || !this._draft?.slug) {
      this._errorMsg = "Bitte speichere die PWA zuerst, bevor du sie installierst.";
      this._render();
      return;
    }
    if (!this._qrInfo?.launch_url) return;
    const url = new URL(this._qrInfo.launch_url, location.origin);
    url.searchParams.set("auto_install", "1");
    window.open(url, "_blank", "noopener");
  }

  _render() {
    if (!this._draft) {
      this.shadowRoot.innerHTML = `
        <style>:host{display:block;padding:24px;color:var(--primary-text-color,#fff);background:var(--primary-background-color,#111827);min-height:100vh;}</style>
        <div>${this._esc(this._errorMsg || "Lade PWA Web-App Studio...")}</div>
      `;
      return;
    }

    const d = this._draft;
    const index = STEPS.findIndex(step => step.id === this._activeTab);
    const step = STEPS[index];
    const detected = this._detectCurrentDevice();
    const dimBase = DEVICE_DIMENSIONS[this._previewDevice] || DEVICE_DIMENSIONS.smartphone;
    const frameW =
      this._previewRotated && this._previewDevice !== "desktop"
        ? dimBase.height
        : dimBase.width;
    const frameH =
      this._previewRotated && this._previewDevice !== "desktop"
        ? dimBase.width
        : dimBase.height;

    const selectedDash = this._dashboards.find(
      (db) => db.url_path === d.content.dashboard_url_path
    );
    const dashViews = selectedDash?.views || [];

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: var(--primary-background-color, #0f172a);
          color: var(--primary-text-color, #f8fafc);
          font-family: var(--paper-font-body1_-_font-family, system-ui, sans-serif);
          box-sizing: border-box;
        }
        * { box-sizing: border-box; }
        .topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 18px;
          background: var(--app-header-background-color, #1e293b);
          border-bottom: 1px solid var(--divider-color, rgba(255,255,255,0.12));
          gap: 12px;
        }
        .studio-logo { width:40px; height:40px; flex:none; object-fit:contain; }
        .topbar-left {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .menu-btn {
          display: none;
          background: transparent;
          border: 1px solid var(--divider-color, rgba(255,255,255,0.2));
          color: inherit;
          border-radius: 8px;
          padding: 6px 10px;
          cursor: pointer;
        }
        @media (max-width: 870px) {
          .menu-btn { display: inline-flex; align-items: center; }
        }
        .workspace {
          display: grid;
          grid-template-columns: 240px minmax(360px, 1.15fr) minmax(340px, 1fr);
          flex: 1;
          min-height: 0;
          overflow: hidden;
        }
        @media (max-width: 1240px) {
          .workspace {
            grid-template-columns: 220px 1fr;
            overflow-y: auto;
          }
          .preview-pane {
            grid-column: 1 / -1;
            min-height: 540px;
          }
        }
        @media (max-width: 780px) {
          .workspace {
            grid-template-columns: 1fr;
          }
        }
        .apps-pane {
          border-right: 1px solid var(--divider-color, rgba(255,255,255,0.12));
          background: var(--card-background-color, #1e293b);
          padding: 14px;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .app-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 10px 12px;
          border-radius: 10px;
          border: 1px solid var(--divider-color, rgba(255,255,255,0.1));
          cursor: pointer;
          background: rgba(255,255,255,0.02);
        }
        .app-item.active {
          border-color: var(--studio-accent);
          background: color-mix(in srgb, var(--studio-accent) 14%, transparent);
        }
        .editor-pane {
          padding: 16px;
          overflow-y: auto;
          border-right: 1px solid var(--divider-color, rgba(255,255,255,0.12));
        }
        .preview-pane {
          padding: 16px;
          overflow: auto;
          background: rgba(0, 0, 0, 0.16);
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
        }
        .tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
          margin-bottom: 14px;
        }
        .tab {
          padding: 8px 12px;
          border-radius: 8px;
          border: 1px solid var(--divider-color, rgba(255,255,255,0.16));
          background: var(--card-background-color, #1e293b);
          color: inherit;
          cursor: pointer;
          font-size: 13px;
        }
        .tab.active {
          background: var(--studio-accent);
          color: #fff;
          border-color: transparent;
        }
        .card-box {
          background: var(--card-background-color, #1e293b);
          border: 1px solid var(--divider-color, rgba(255,255,255,0.12));
          border-radius: 12px;
          padding: 14px;
          margin-bottom: 14px;
        }
        .field-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
          gap: 10px;
        }
        label {
          display: flex;
          flex-direction: column;
          gap: 5px;
          font-size: 12px;
          color: var(--secondary-text-color, #94a3b8);
        }
        label.inline {
          flex-direction: row;
          align-items: center;
          gap: 8px;
          color: var(--primary-text-color, #f8fafc);
          font-size: 13px;
        }
        input, select, textarea {
          width: 100%;
          padding: 8px 10px;
          border-radius: 8px;
          border: 1px solid var(--divider-color, rgba(255,255,255,0.2));
          background: var(--primary-background-color, #0f172a);
          color: var(--primary-text-color, #f8fafc);
          font-size: 13px;
          font-family: inherit;
        }
        input[type="checkbox"] {
          width: auto;
        }
        input[type="color"] {
          padding: 2px;
          height: 36px;
        }
        .btn {
          padding: 8px 14px;
          border-radius: 8px;
          border: 1px solid var(--divider-color, rgba(255,255,255,0.2));
          background: var(--card-background-color, #1e293b);
          color: var(--primary-text-color, #f8fafc);
          cursor: pointer;
          font-size: 13px;
          font-weight: 500;
        }
        .btn.primary {
          background: var(--studio-accent);
          color: #fff;
          border-color: transparent;
        }
        .btn.danger {
          background: #b91c1c;
          color: #fff;
          border-color: transparent;
        }
        .card-list-item {
          border: 1px solid var(--divider-color, rgba(255,255,255,0.16));
          border-radius: 10px;
          padding: 10px;
          margin-top: 8px;
          background: rgba(255,255,255,0.03);
        }
        .device-toolbar {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          align-items: center;
          justify-content: center;
        }
        .device-bezel-wrap {
          width: 100%;
          display: flex;
          justify-content: center;
          overflow: auto;
          padding: 8px;
        }
        .device-bezel {
          width: ${frameW}px;
          height: ${frameH}px;
          transform: scale(${dimBase.scale});
          transform-origin: top center;
          border: 10px solid #334155;
          border-radius: ${this._previewDevice === "desktop" ? "14px" : "30px"};
          background: ${this._esc(d.manifest.background_color)};
          box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-shrink: 0;
        }
        .device-header {
          display: ${d.manifest.kiosk_mode || d.manifest.hide_ha_header ? "none" : "flex"};
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          background: ${this._esc(d.manifest.theme_color)};
          color: #ffffff;
          font-weight: 600;
        }
        #preview-stage {
          padding: 14px;
          display: grid;
          gap: 12px;
          overflow-y: auto;
          flex: 1;
          align-content: start;
        }
        .preview-empty, .preview-err {
          padding: 16px;
          border-radius: 10px;
          background: var(--card-background-color, #1e293b);
          grid-column: 1 / -1;
        }
        .banner-ok {
          padding: 8px 12px;
          border-radius: 8px;
          background: rgba(16, 185, 129, 0.2);
          border: 1px solid #10b981;
          margin-bottom: 10px;
          font-size: 13px;
        }
        .banner-err {
          padding: 8px 12px;
          border-radius: 8px;
          background: rgba(239, 68, 68, 0.2);
          border: 1px solid #ef4444;
          margin-bottom: 10px;
          font-size: 13px;
        }
        :host {height:100dvh;max-height:100%;min-height:0;--studio-accent:${STUDIO_ACCENT};}
        .mobile-nav {display:none}
        .topbar {background:var(--card-background-color);color:var(--primary-text-color)}
        .topbar button,.step-actions button { font-size:.875rem; }
        input[type=checkbox] { accent-color:var(--studio-accent); }
        .topbar button,.device-toolbar button {min-height:44px;white-space:nowrap;border-radius:22px}
        .card-box {border-radius:20px;padding:clamp(14px,2vw,24px)}
        button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible {outline:3px solid var(--studio-accent);outline-offset:2px}
        .device-bezel-wrap {position:relative;overflow:hidden;flex:none}
        .device-bezel {position:absolute;left:50%;translate:-50% 0}
        @media(max-width:1240px) {
          :host {display:grid;grid-template-rows:auto minmax(0,1fr) auto;overflow:hidden}
          .topbar {padding:8px 12px;gap:6px;flex-wrap:wrap}
          .topbar-left {gap:6px}
          .studio-logo {width:34px;height:34px}
          .topbar strong {font-size:15px!important}
          .menu-btn {display:inline-flex;align-items:center;justify-content:center;min-width:44px}
          .topbar .btn {padding:8px 12px}
          .workspace {display:block;min-width:0;overflow:hidden}
          .workspace > * {display:none;height:100%;min-height:0;min-width:0;border:0;overflow:auto;overscroll-behavior:contain}
          .workspace[data-pane=apps] .apps-pane,.workspace[data-pane=editor] .editor-pane,.workspace[data-pane=preview] .preview-pane {display:block}
          .mobile-nav {display:flex;justify-content:space-around;background:var(--card-background-color);border-top:1px solid var(--divider-color);padding:4px 8px max(4px,env(safe-area-inset-bottom))}
          .mobile-nav button {flex:1;display:grid;justify-items:center;gap:2px;padding:4px;border:0;background:transparent;color:inherit;font:inherit;font-size:12px;cursor:pointer}
          .mobile-nav ha-icon {width:64px;padding:3px 20px;box-sizing:border-box;border-radius:18px}
          .mobile-nav [aria-pressed=true] ha-icon {background:color-mix(in srgb,var(--studio-accent) 24%,transparent);color:var(--studio-accent)}
          .tabs {flex-wrap:nowrap;overflow-x:auto;padding:3px 0 7px}
          .field-grid {grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr))}
          input:not([type=checkbox]),select,textarea {font-size:16px;min-height:44px}
          .preview-pane > * {margin-bottom:12px}
        }
        .step-nav { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:3px; margin-bottom:16px; }
        .step-nav button { display:grid; justify-items:center; gap:4px; background:transparent; color:inherit; border:0; border-radius:14px; padding:8px 0; min-height:50px; font:inherit; font-size:.8rem; cursor:pointer; }
        .step-nav [aria-current] { background:color-mix(in srgb,var(--studio-accent) 19%,var(--card-background-color,#1e293b)); font-weight:700; }
        .step-nav [aria-current] ha-icon { color:var(--primary-text-color); }
        .step-header { position:relative; isolation:isolate; overflow:hidden; padding:clamp(18px,3vw,32px); margin-bottom:16px; border-radius:24px;
          background:linear-gradient(115deg,color-mix(in srgb,var(--studio-accent) 18%,var(--card-background-color,#1e293b)),var(--card-background-color,#1e293b)); }
        .step-header::after { content:""; position:absolute; z-index:-1; right:-74px; top:-94px; width:160px; height:160px; border-radius:50%;
          border:18px solid color-mix(in srgb,var(--studio-accent) 9%,transparent); outline:1px solid color-mix(in srgb,var(--studio-accent) 22%,transparent); }
        .step-header > span { font-size:.8rem; font-weight:650; }
        .step-header h1 { margin:.4rem 0; line-height:1.13; font-size:clamp(1.55rem,3vw,2.1rem); letter-spacing:-.035em; }
        .step-header p,.guest-note p { margin:0; line-height:1.55; }
        .step-actions { display:flex; align-items:center; justify-content:flex-end; gap:8px; padding:4px 0 16px; }
        .step-actions button,summary,.access-user { min-height:44px; }
        .step-actions button { border-radius:24px; }
        details { margin-top:16px; border-top:1px solid var(--divider-color,#8885); }
        summary { padding:12px 0; cursor:pointer; font-weight:600; }
        #launch-sample { position:relative; height:17rem; overflow:hidden; border-radius:18px; }
        .card-box svg { max-width:100%; height:auto; }
        .guest-note { margin:14px 0; padding:16px; border-radius:16px; background:color-mix(in srgb,var(--studio-accent) 10%,var(--card-background-color,#1e293b)); }
        .guest-note button { min-height:44px; margin:4px 0; }
        .guest-note a { color:inherit; text-underline-offset:3px; }
        .companion-link { display:inline-flex; align-items:center; min-height:44px; text-decoration:none; }
        .companion-card p { margin:8px 0 14px; line-height:1.5; }
        .share-actions { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
        .share-actions .btn { min-height:44px; }
        .access-user { display:flex; align-items:center; gap:10px; }
        .editor-pane input,.editor-pane select { min-width:0; }
      </style>

      <div class="topbar">
        <div class="topbar-left">
          <button class="menu-btn" id="toggle-menu-btn" aria-label="Menü öffnen"><ha-icon icon="mdi:menu"></ha-icon></button>
          <img class="studio-logo" src="${STUDIO_LOGO}" width="40" height="40" alt="" />
          <strong style="font-size:17px;">PWA Web-App Studio</strong>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <button class="btn" id="new-app-btn">+ Neue PWA</button>
          <button class="btn primary" id="save-app-btn">Speichern</button>
        </div>
      </div>

      <div class="workspace" data-pane="${this._mobilePane}">
        <aside class="apps-pane">
          <strong style="font-size:12px;text-transform:uppercase;opacity:0.7;">Deine PWAs</strong>
          ${
            this._apps.length === 0
              ? `<div style="font-size:13px;opacity:0.7;">Noch keine App gespeichert.</div>`
              : this._apps
                  .map(
                    (app) => `
                <div class="app-item ${app.app_id === this._selectedAppId ? "active" : ""}" data-appid="${this._esc(app.app_id)}">
                  <div>
                    <div style="font-weight:600;font-size:13px;">${this._esc(app.manifest.name)}</div>
                    <div style="font-size:11px;opacity:0.7;">/${this._esc(app.slug)}/ • v${app.version}</div>
                  </div>
                  <button class="btn danger del-app-btn" data-del="${this._esc(app.app_id)}" style="padding:4px 8px;font-size:11px;">✕</button>
                </div>`
                  )
                  .join("")
          }
        </aside>

        <section class="editor-pane">
          ${this._statusMsg ? `<div class="banner-ok" role="status">${this._esc(this._statusMsg)}</div>` : ""}
          ${this._errorMsg ? `<div class="banner-err" role="alert">${this._esc(this._errorMsg)}</div>` : ""}

          <nav class="step-nav" aria-label="Einrichtungsschritte">
            ${STEPS.map((item, i) => `<button data-tab="${item.id}" aria-label="Schritt ${i + 1}: ${item.label}" ${item === step ? 'aria-current="step"' : ""}>
              <ha-icon icon="mdi:${item.icon}" aria-hidden="true"></ha-icon><span>${item.label}</span>
            </button>`).join("")}
          </nav>
          <header class="step-header">
            <span>Schritt ${index + 1} von ${STEPS.length}</span>
            <h1 id="step-title" tabindex="-1">${step.title}</h1>
            <p>${step.hint}</p>
          </header>
          ${this._renderActiveTabHtml(d, dashViews, detected)}
          <div class="step-actions">
            ${index ? `<button class="btn" data-tab="${STEPS[index - 1].id}">Zurück</button>` : ""}
            ${index + 1 < STEPS.length
              ? `<button class="btn primary" data-tab="${STEPS[index + 1].id}">Weiter zu ${STEPS[index + 1].label} →</button>`
              : `<button class="btn primary" id="finish-btn">App speichern</button>`}
          </div>
        </section>

        <aside class="preview-pane">
          <div class="device-toolbar">
            <button class="tab ${this._previewDevice === "desktop" ? "active" : ""}" data-dev="desktop">Computer</button>
            <button class="tab ${this._previewDevice === "tablet" ? "active" : ""}" data-dev="tablet">Tablet</button>
            <button class="tab ${this._previewDevice === "smartphone" ? "active" : ""}" data-dev="smartphone">Smartphone</button>
            ${
              this._previewDevice !== "desktop"
                ? `<button class="btn" id="rotate-dev-btn">⟳ Drehen</button>`
                : ""
            }
          </div>
          <div style="font-size:12px;opacity:0.75;">
            Vorschau: ${dimBase.label} (${frameW}×${frameH}px) • Erkannt: ${this._esc(detected.osLabel)}
          </div>
          <div class="device-bezel-wrap">
            <div class="device-bezel">
              <div class="device-header">
                <span>${this._esc(d.manifest.name)}</span>
                <span style="font-size:12px;opacity:0.9;">${this._esc(d.manifest.display)}</span>
              </div>
              <div id="preview-stage"></div>
            </div>
          </div>
        </aside>
      </div>
      <nav class="mobile-nav" aria-label="Studio">
        ${[["apps","view-grid-outline","Apps"],["editor","pencil-outline","Editor"],["preview","cellphone","Vorschau"]].map(([key,icon,label]) =>
          `<button data-pane-target="${key}" aria-pressed="${this._mobilePane === key}"><ha-icon icon="mdi:${icon}"></ha-icon>${label}</button>`
        ).join("")}
      </nav>
    `;

    this._bindEvents();
    this._previewObserver?.disconnect();
    const wrap = this.shadowRoot.querySelector(".device-bezel-wrap");
    const bezel = wrap.querySelector(".device-bezel");
    this._previewObserver = new ResizeObserver(([entry]) => {
      const width = entry.contentRect.width;
      if (!width) return;
      const scale = Math.min(1, width / frameW, dimBase.scale);
      bezel.style.transform = "scale(" + scale + ")";
      wrap.style.height = Math.ceil(frameH * scale + 16) + "px";
    });
    this._previewObserver.observe(wrap);
  }

  _renderActiveTabHtml(d, dashViews, detected) {
    if (this._activeTab === "general") {
      return `
        <div class="card-box">
          <div class="field-grid">
            <label>App-Name
              <input id="f-name" value="${this._esc(d.manifest.name)}" />
            </label>
            <label>Kurzname (Homescreen)
              <input id="f-short-name" value="${this._esc(d.manifest.short_name)}" />
            </label>
            <label>Akzentfarbe
              <input type="color" id="f-theme" value="${this._esc(d.manifest.theme_color)}" />
            </label>
            <label>Hintergrundfarbe
              <input type="color" id="f-bg" value="${this._esc(d.manifest.background_color)}" />
            </label>
          </div>
          <label style="margin-top:10px;">Beschreibung
            <input id="f-desc" value="${this._esc(d.manifest.description)}" />
          </label>
          <label style="margin-top:12px">Animation beim Öffnen
            <select id="f-launch">
              ${[["ripple","Sanfte Wellen"],["glow","Leuchtschein"],["still","Ruhiges Standbild"]].map(([key,title]) =>
                `<option value="${key}" ${(d.manifest.launch_style || "ripple") === key ? "selected" : ""}>${title}</option>`).join("")}
            </select>
          </label>
          <details class="launch-preview"><summary>Startanimation ansehen</summary>
            <div id="launch-sample"></div>
          </details>
          <details><summary>Weitere Einstellungen</summary>
          <div class="field-grid">
            <label>URL-Slug (optional)
              <input id="f-slug" placeholder="automatisch" value="${this._esc(d.slug)}" />
            </label>
            <label>Display-Modus
              <select id="f-display">
                ${["standalone", "fullscreen", "minimal-ui", "browser"]
                  .map(
                    (m) =>
                      `<option value="${m}" ${d.manifest.display === m ? "selected" : ""}>${m}</option>`
                  )
                  .join("")}
              </select>
            </label>
            <label>Ausrichtung
              <select id="f-orientation">
                ${["any", "natural", "portrait", "landscape"]
                  .map(
                    (o) =>
                      `<option value="${o}" ${d.manifest.orientation === o ? "selected" : ""}>${o}</option>`
                  )
                  .join("")}
              </select>
            </label>
            <label>Sprache / Richtung
              <div style="display:flex;gap:6px;">
                <input id="f-lang" value="${this._esc(d.manifest.lang)}" style="width:60%;" />
                <select id="f-dir" style="width:40%;">
                  <option value="ltr" ${d.manifest.dir === "ltr" ? "selected" : ""}>LTR</option>
                  <option value="rtl" ${d.manifest.dir === "rtl" ? "selected" : ""}>RTL</option>
                </select>
              </div>
            </label>
          </div>
          <div class="field-grid" style="margin-top:12px;">
            <label class="inline"><input type="checkbox" id="f-offline" ${d.manifest.offline_enabled ? "checked" : ""} /> Startbildschirm offline verfügbar machen</label>
            <label class="inline"><input type="checkbox" id="f-hide-hdr" ${d.manifest.hide_ha_header ? "checked" : ""} /> PWA-Header ausblenden</label>
            <label class="inline"><input type="checkbox" id="f-kiosk" ${d.manifest.kiosk_mode ? "checked" : ""} /> Kiosk-Vollmodus</label>
          </div></details>
        </div>
      `;
    }

    if (this._activeTab === "content") {
      const importedCards = [];
      for (const db of this._dashboards) {
        for (const vw of db.views || []) {
          for (const card of vw.cards || []) {
            importedCards.push({
              label: `${db.title} / ${vw.title}: ${card.title || card.name || card.type}`,
              config: card,
            });
          }
        }
      }

      return `
        <div class="card-box">
          <div class="field-grid">
            <label>Inhaltsquelle
              <select id="c-source-mode">
                <option value="lovelace_dashboard" ${d.content.source_mode === "lovelace_dashboard" ? "selected" : ""}>Ein vorhandenes Dashboard</option>
                <option value="lovelace_cards" ${d.content.source_mode === "lovelace_cards" ? "selected" : ""}>Einzelne Karten zusammenstellen</option>
              </select>
            </label>
            <label>Layout-Modus
              <select id="c-layout-mode">
                <option value="grid" ${d.content.layout_mode === "grid" ? "selected" : ""}>Grid (Spalten)</option>
                <option value="stack" ${d.content.layout_mode === "stack" ? "selected" : ""}>Vertikaler Stapel (1 Spalte)</option>
                <option value="masonry" ${d.content.layout_mode === "masonry" ? "selected" : ""}>Masonry</option>
              </select>
            </label>
            <label>Spalten (Tablet/Desktop)
              <input type="number" min="1" max="4" id="c-grid-cols" value="${d.content.grid_columns}" />
            </label>
            <label>Standard-Vorschaugerät
              <select id="c-default-dev">
                <option value="desktop" ${d.content.default_preview_device === "desktop" ? "selected" : ""}>Computer</option>
                <option value="tablet" ${d.content.default_preview_device === "tablet" ? "selected" : ""}>Tablet</option>
                <option value="smartphone" ${d.content.default_preview_device === "smartphone" ? "selected" : ""}>Smartphone</option>
              </select>
            </label>
          </div>
        </div>

        ${
          d.content.source_mode === "lovelace_dashboard"
            ? `
          <div class="card-box">
            <div class="field-grid">
              <label>Lovelace Dashboard auswählen
                <select id="c-dashboard">
                  ${this._dashboards
                    .map(
                      (db) =>
                        `<option value="${this._esc(db.url_path)}" ${d.content.dashboard_url_path === db.url_path ? "selected" : ""}>${this._esc(db.title)} (/${this._esc(db.url_path)})</option>`
                    )
                    .join("")}
                </select>
              </label>
              <label>Ziel-Ansicht (View, optional)
                <select id="c-view-path">
                  <option value="">Alle Views / Standard-View</option>
                  ${dashViews
                    .map(
                      (vw) =>
                        `<option value="${this._esc(vw.path)}" ${String(d.content.view_path) === String(vw.path) ? "selected" : ""}>${this._esc(vw.title)} (${this._esc(vw.path)})</option>`
                    )
                    .join("")}
                </select>
              </label>
            </div>
            <div style="margin-top:12px;">
              <button class="btn" id="c-import-view-btn">Karten dieser View als bearbeitbare Liste übernehmen</button>
            </div>
          </div>`
            : `
          <div class="card-box">
            <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end;">
              <label style="flex:1;min-width:190px;">Vorhandene Karte aus Dashboard übernehmen
                <select id="c-import-select">
                  <option value="">-- Karte wählen --</option>
                  ${importedCards
                    .map(
                      (item, idx) => `<option value="${idx}">${this._esc(item.label)}</option>`
                    )
                    .join("")}
                </select>
              </label>
              <button class="btn" id="c-import-btn">Hinzufügen</button>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;">
              ${Object.entries(this._cardPresets())
                .map(
                  ([key, val]) =>
                    `<button class="btn preset-add-btn" data-preset="${key}">+ ${this._esc(val.label)}</button>`
                )
                .join("")}
            </div>
          </div>

          <div class="card-box">
            <strong>Karten-Reihenfolge (${d.content.cards.length} Karten — Drag & Drop oder Pfeile)</strong>
            ${
              d.content.cards.length === 0
                ? `<div style="font-size:13px;opacity:0.7;margin-top:8px;">Noch keine Karten hinzugefügt.</div>`
                : d.content.cards
                    .map(
                      (card, idx) => `
                  <div class="card-list-item" draggable="true" data-card-idx="${idx}">
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
                      <strong>#${idx + 1} ${this._esc(card.title || card.config?.type || "Karte")}</strong>
                      <div style="display:flex;gap:4px;align-items:center;">
                        <select class="card-span-sel" data-idx="${idx}" style="width:92px;padding:4px;">
                          ${[1, 2, 3, 4]
                            .map(
                              (sp) =>
                                `<option value="${sp}" ${card.col_span === sp ? "selected" : ""}>${sp} Spalte(n)</option>`
                            )
                            .join("")}
                        </select>
                        <button class="btn card-up-btn" data-idx="${idx}">▲</button>
                        <button class="btn card-dn-btn" data-idx="${idx}">▼</button>
                        <button class="btn danger card-rm-btn" data-idx="${idx}">✕</button>
                      </div>
                    </div>
                    <textarea class="card-json-edit" data-idx="${idx}" rows="4" style="margin-top:8px;font-family:monospace;font-size:12px;">${this._esc(JSON.stringify(card.config, null, 2))}</textarea>
                  </div>`
                    )
                    .join("")
            }
          </div>`
        }
      `;
    }

    if (this._activeTab === "icon") {
      const ic = d.icon;
      const cornerOpts = [
        ["bottom_right", "Unten rechts"],
        ["top_right", "Oben rechts"],
        ["bottom_left", "Unten links"],
        ["top_left", "Oben links"],
      ];
      return `
        <div class="card-box" style="display:flex;gap:16px;align-items:center;">
          <img id="live-icon-img" src="${this._iconPreviewUrl || ""}" alt="Icon Vorschau" style="width:96px;height:96px;border-radius:20px;border:1px solid rgba(255,255,255,0.2);background:#0f172a;object-fit:cover;" />
          <div style="flex:1;display:flex;flex-direction:column;gap:8px;">
            <label>Icon-Modus
              <select id="i-mode">
                <option value="ha_default" ${ic.mode === "ha_default" ? "selected" : ""}>Offizielles Home Assistant App-Icon</option>
                <option value="mdi_icon" ${ic.mode === "mdi_icon" ? "selected" : ""}>Home Assistant / MDI Icon</option>
                <option value="ha_with_badge" ${ic.mode === "ha_with_badge" ? "selected" : ""}>HA App-Icon + kleines selektiertes Icon in Ecke</option>
                <option value="icon_with_ha_badge" ${ic.mode === "icon_with_ha_badge" ? "selected" : ""}>Selektiertes/Upload Icon + kleines HA Icon in Ecke</option>
                <option value="uploaded" ${ic.mode === "uploaded" ? "selected" : ""}>Eigenes App-Icon hochladen</option>
                <option value="dashboard_default" ${ic.mode === "dashboard_default" ? "selected" : ""}>Standard-Icon des gewählten Lovelace Dashboards</option>
              </select>
            </label>
            <button class="btn" id="i-use-dash-icon-btn">Dashboard-Icon in Haupt-MDI übernehmen</button>
          </div>
        </div>

        <div class="card-box">
          <div class="field-grid">
            <label>Haupt-MDI-Icon (z. B. mdi:sofa)
              <input id="i-mdi" value="${this._esc(ic.mdi_icon)}" />
            </label>
            <label>Icon-Vordergrundfarbe
              <input type="color" id="i-fg" value="${this._esc(ic.icon_color)}" />
            </label>
            <label>Icon-Hintergrundfarbe
              <input type="color" id="i-bg" value="${this._esc(ic.bg_color)}" />
            </label>
            <label>Ecken-Abrundung (%)
              <input type="number" min="0" max="50" id="i-radius" value="${ic.corner_radius_pct}" />
            </label>
            <label>Badge-MDI-Icon
              <input id="i-badge-mdi" value="${this._esc(ic.badge_icon)}" />
            </label>
            <label>Badge-Ecke
              <select id="i-badge-pos">
                ${cornerOpts
                  .map(
                    ([v, lbl]) =>
                      `<option value="${v}" ${ic.badge_position === v ? "selected" : ""}>${lbl}</option>`
                  )
                  .join("")}
              </select>
            </label>
            <label>Badge-Icon-Farbe
              <input type="color" id="i-badge-fg" value="${this._esc(ic.badge_color)}" />
            </label>
            <label>Badge-Hintergrundfarbe
              <input type="color" id="i-badge-bg" value="${this._esc(ic.badge_bg_color)}" />
            </label>
          </div>
          <div style="margin-top:12px;">
            <label>Eigenes Icon hochladen (PNG / JPEG / WebP)
              <input type="file" id="i-upload" accept="image/png,image/jpeg,image/webp" />
            </label>
          </div>
        </div>
      `;
    }

    if (this._activeTab === "access") {
      const mode = d.access.require_admin ? "admin" : d.access.local_guests ? "guest"
        : d.access.allow_all_authenticated ? "all" : "selected";
      const selectable = this._users.filter(u => !u.is_admin && (mode !== "guest" || u.local_only));
      return `
        <div class="card-box">
          <label>Freigabe für diese App
            <select id="access-mode">
              ${[["all","Alle angemeldeten Personen"],["selected","Ausgewählte Personen"],["guest","🏡 Gäste im Heimnetz"],["admin","Nur Administratoren"]].map(([key,title]) =>
                `<option value="${key}" ${mode === key ? "selected" : ""}>${title}</option>`).join("")}
            </select>
          </label>
          ${mode === "guest" ? `<div class="guest-note"><p><strong>Gäste einrichten</strong></p>
            <ol><li>Erstelle für deinen Gast ein Konto ohne Administratorrechte. Aktiviere „Nur lokaler Zugriff“.</li>
            <li>Wähle das Konto hier aus und speichere die App.</li>
            <li>Der Gast meldet sich im Heim-WLAN in seiner Companion-App an und öffnet den Companion-Link aus dem Schritt „Teilen“.</li></ol>
            <a href="/config/users" target="_blank" rel="noopener">Benutzerverwaltung öffnen ↗</a>
            <button type="button" class="btn" id="reload-users">Konten neu laden</button>
            <p>Das Konto behält seine übrigen Home-Assistant-Rechte.</p></div>` : ""}
          ${mode === "selected" || mode === "guest" ? `<fieldset><legend>Konten auswählen</legend>
            ${selectable.map(u => `<label class="access-user"><input type="checkbox" class="a-user-cb" value="${this._esc(u.id)}"
                ${d.access.allowed_user_ids.includes(u.id) ? "checked" : ""} />${this._esc(u.name)}</label>`).join("") || "<p>Kein passendes Konto vorhanden.</p>"}
            </fieldset>` : ""}
          <p>Administratoren können die App jederzeit öffnen.</p>
        </div>
      `;
    }

    const saved = this._apps.find(app => app.app_id === this._selectedAppId);
    const runnerPath = saved ? `/pwa-app-studio-runner/${saved.slug}` : "";
    const companionUrl = runnerPath ? `homeassistant://navigate${runnerPath}` : "";
    return `
      <div class="card-box companion-card">
        <strong>In der Home Assistant Companion-App öffnen</strong>
        ${companionUrl ? `
          <p>Öffne die App auf deinem Handy mit der Anmeldung, die du dort in Home Assistant schon verwendest.</p>
          <div class="share-actions">
            <a class="btn primary companion-link" href="${this._esc(companionUrl)}">In Home Assistant öffnen ↗</a>
            <button type="button" class="btn" id="copy-companion-link">Companion-Link kopieren</button>
          </div>
          <p id="companion-copy-status" role="status" hidden></p>
          <details id="companion-link-details">
            <summary>Link und Dashboard-Pfad anzeigen</summary>
            <label>Companion-Link zum Weitergeben
              <input id="companion-url" type="text" readonly value="${this._esc(companionUrl)}" />
            </label>
            <label>Pfad für eine Schaltfläche im Home-Assistant-Dashboard
              <input type="text" readonly value="${this._esc(runnerPath)}" />
            </label>
          </details>` : "<p>Speichere deine App, um den Companion-Link zu erhalten.</p>"}
      </div>
      <div class="card-box">
        <strong>Als Web-App auf dem Startbildschirm installieren</strong>
        <p style="font-size:13px;opacity:0.85;">
          Dein Gerät: <b>${this._esc(detected.osLabel)}</b>
        </p>
        <div style="display:flex;flex-wrap:wrap;gap:10px;">
          <button class="btn primary" id="install-current-btn" ${this._qrInfo ? "" : "disabled"}>Auf diesem Gerät installieren</button>
          ${
            this._selectedAppId
              ? `<button class="btn" id="refresh-qr-btn">QR-Code aktualisieren</button>`
              : ""
          }
        </div>
      </div>

      <div class="card-box">
        <strong>QR-Code für die Browser-Web-App</strong>
        ${
          !this._selectedAppId
            ? `<p style="font-size:13px;opacity:0.75;">Bitte speichere die App zunächst über "Speichern", um einen QR-Code zu erzeugen.</p>`
            : !this._qrInfo
            ? `<p style="font-size:13px;opacity:0.75;">${this._errorMsg ? "QR-Code aktuell nicht verfügbar." : "QR-Code wird geladen …"}</p>`
            : `
          <div style="display:flex;flex-wrap:wrap;gap:18px;align-items:flex-start;margin-top:12px;">
            <div style="background:#ffffff;padding:12px;border-radius:12px;width:210px;height:210px;display:flex;align-items:center;justify-content:center;">
              ${this._qrInfo.qr_svg}
            </div>
            <div style="flex:1;min-width:220px;">
              <div style="font-size:12px;opacity:0.75;">Ziel-URL zum Scannen:</div>
              <input readonly value="${this._esc(this._qrInfo.launch_url)}" style="margin:6px 0 12px;" onclick="this.select()" />
              <div style="font-size:12px;opacity:0.75;margin-bottom:6px;">Berechtigte Benutzer nach Scan:</div>
              <div style="display:flex;flex-wrap:wrap;gap:6px;">
                ${(this._qrInfo.permitted_users || [])
                  .map(
                    (u) =>
                      `<span style="font-size:12px;padding:4px 8px;border-radius:999px;background:rgba(3,169,244,0.18);border:1px solid rgba(3,169,244,0.4);">${this._esc(u.name)}</span>`
                  )
                  .join("")}
              </div>
            </div>
          </div>`
        }
      </div>
    `;
  }

  _bindEvents() {
    const sr = this.shadowRoot;
    const sample = sr.getElementById("launch-sample");
    if (sample) {
      const shadow = sample.attachShadow({ mode: "open" });
      shadow.innerHTML = `<link rel="stylesheet" href="/pwa_app_studio_static/pwa-shell.css">
        <div class="launch" aria-hidden="true" style="color:white">
          <div class="welcome"><div class="mark"><span style="font-size:48px">⌂</span></div>
          <h1></h1><p>Deine App wird geöffnet …</p></div></div>`;
      const updateSample = () => {
        const manifest = this._draft.manifest;
        sample.style.setProperty("--app-accent", manifest.theme_color);
        sample.style.setProperty("--app-bg", manifest.background_color);
        shadow.querySelector(".launch").dataset.style = manifest.launch_style || "ripple";
        shadow.querySelector("h1").textContent = manifest.name;
        if (this._iconPreviewUrl) this._updateSampleIcon(sample);
      };
      sr.querySelector(".launch-preview").ontoggle = updateSample;
      sr.querySelector(".editor-pane").addEventListener("input", updateSample);
      updateSample();
    }
    for (const button of sr.querySelectorAll("[data-pane-target]")) {
      button.onclick = () => {
        this._mobilePane = button.dataset.paneTarget;
        sr.querySelector(".workspace").dataset.pane = this._mobilePane;
        for (const item of sr.querySelectorAll("[data-pane-target]")) {
          item.setAttribute("aria-pressed", String(item === button));
        }
      };
    }
    sr.getElementById("toggle-menu-btn")?.addEventListener("click", () => {
      this.dispatchEvent(new CustomEvent("hass-toggle-menu", { bubbles: true, composed: true }));
    });
    sr.getElementById("new-app-btn")?.addEventListener("click", () => this._newAppDraft());
    sr.getElementById("finish-btn")?.addEventListener("click", () => this._saveApp());
    sr.getElementById("save-app-btn")?.addEventListener("click", () => this._saveApp());

    sr.querySelectorAll(".app-item").forEach((el) => {
      el.addEventListener("click", (ev) => {
        if (ev.target.classList.contains("del-app-btn")) return;
        this._selectApp(el.dataset.appid);
      });
    });
    sr.querySelectorAll(".del-app-btn").forEach((btn) => {
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        this._deleteApp(btn.dataset.del);
      });
    });

    sr.querySelectorAll("button[data-tab]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this._activeTab = btn.dataset.tab;
        this._render();
        sr.querySelector(".editor-pane").scrollTop = 0;
        sr.getElementById("step-title").focus({ preventScroll: true });
        this._renderDevicePreviewCards();
        if (this._activeTab === "icon") this._refreshIconPreview();
        if (this._activeTab === "distribute" && this._selectedAppId) this._loadQrCode();
      });
    });

    sr.querySelectorAll("[data-dev]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this._previewDevice = btn.dataset.dev;
        this._previewRotated = false;
        this._render();
        this._renderDevicePreviewCards();
      });
    });
    sr.getElementById("rotate-dev-btn")?.addEventListener("click", () => {
      this._previewRotated = !this._previewRotated;
      this._render();
      this._renderDevicePreviewCards();
    });

    const bindVal = (id, fn, rerenderPreview = false) => {
      sr.getElementById(id)?.addEventListener("input", (e) => {
        fn(e.target.value);
        if (rerenderPreview) {
          this._render();
          this._renderDevicePreviewCards();
        }
      });
    };
    const bindChk = (id, fn, rerenderPreview = false) => {
      sr.getElementById(id)?.addEventListener("change", (e) => {
        fn(e.target.checked);
        if (rerenderPreview) {
          this._render();
          this._renderDevicePreviewCards();
        }
      });
    };

    bindVal("f-name", (v) => (this._draft.manifest.name = v));
    bindVal("f-short-name", (v) => (this._draft.manifest.short_name = v));
    bindVal("f-slug", (v) => (this._draft.slug = v));
    bindVal("f-launch", (v) => (this._draft.manifest.launch_style = v));
    bindVal("f-display", (v) => (this._draft.manifest.display = v));
    bindVal("f-orientation", (v) => (this._draft.manifest.orientation = v));
    bindVal("f-lang", (v) => (this._draft.manifest.lang = v));
    bindVal("f-dir", (v) => (this._draft.manifest.dir = v));
    bindVal("f-theme", (v) => (this._draft.manifest.theme_color = v), true);
    bindVal("f-bg", (v) => (this._draft.manifest.background_color = v), true);
    bindVal("f-desc", (v) => (this._draft.manifest.description = v));
    bindChk("f-offline", (v) => (this._draft.manifest.offline_enabled = v));
    bindChk("f-hide-hdr", (v) => (this._draft.manifest.hide_ha_header = v), true);
    bindChk("f-kiosk", (v) => (this._draft.manifest.kiosk_mode = v), true);

    sr.getElementById("c-source-mode")?.addEventListener("change", (e) => {
      this._draft.content.source_mode = e.target.value;
      this._render();
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-layout-mode")?.addEventListener("change", (e) => {
      this._draft.content.layout_mode = e.target.value;
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-grid-cols")?.addEventListener("change", (e) => {
      this._draft.content.grid_columns = Number(e.target.value || 2);
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-default-dev")?.addEventListener("change", (e) => {
      this._draft.content.default_preview_device = e.target.value;
      this._previewDevice = e.target.value;
      this._render();
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-dashboard")?.addEventListener("change", (e) => {
      this._draft.content.dashboard_url_path = e.target.value;
      this._draft.content.view_path = "";
      this._render();
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-view-path")?.addEventListener("change", (e) => {
      this._draft.content.view_path = e.target.value;
      this._renderDevicePreviewCards();
    });
    sr.getElementById("c-import-view-btn")?.addEventListener("click", () =>
      this._importWholeDashboardViewAsCards()
    );

    sr.getElementById("c-import-btn")?.addEventListener("click", () => {
      const sel = sr.getElementById("c-import-select");
      const idx = sel?.value;
      if (idx === "" || idx === undefined) return;
      const flat = [];
      for (const db of this._dashboards) {
        for (const vw of db.views || []) {
          for (const card of vw.cards || []) flat.push(card);
        }
      }
      if (flat[Number(idx)]) this._importCardFromDashboard(flat[Number(idx)]);
    });

    sr.querySelectorAll(".preset-add-btn").forEach((btn) => {
      btn.addEventListener("click", () => this._addPresetCard(btn.dataset.preset));
    });

    sr.querySelectorAll(".card-up-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.idx);
        this._reorderCard(i, i - 1);
      });
    });
    sr.querySelectorAll(".card-dn-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.idx);
        this._reorderCard(i, i + 1);
      });
    });
    sr.querySelectorAll(".card-rm-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.idx);
        this._draft.content.cards.splice(i, 1);
        this._render();
        this._renderDevicePreviewCards();
      });
    });
    sr.querySelectorAll(".card-span-sel").forEach((sel) => {
      sel.addEventListener("change", (e) => {
        const i = Number(sel.dataset.idx);
        this._draft.content.cards[i].col_span = Number(e.target.value || 1);
        this._renderDevicePreviewCards();
      });
    });
    sr.querySelectorAll(".card-json-edit").forEach((ta) => {
      ta.addEventListener("change", (e) => {
        const i = Number(ta.dataset.idx);
        try {
          this._draft.content.cards[i].config = JSON.parse(e.target.value);
          this._errorMsg = "";
          this._renderDevicePreviewCards();
        } catch (err) {
          this._errorMsg = `Ungültiges JSON in Karte #${i + 1}: ${err.message}`;
        }
      });
    });

    sr.querySelectorAll(".card-list-item[draggable]").forEach((row) => {
      row.addEventListener("dragstart", () => {
        this._dragCardIndex = Number(row.dataset.cardIdx);
      });
      row.addEventListener("dragover", (ev) => ev.preventDefault());
      row.addEventListener("drop", (ev) => {
        ev.preventDefault();
        const targetIdx = Number(row.dataset.cardIdx);
        if (this._dragCardIndex !== null && this._dragCardIndex !== targetIdx) {
          this._reorderCard(this._dragCardIndex, targetIdx);
        }
        this._dragCardIndex = null;
      });
    });

    const bindIcon = (id, fn) => {
      sr.getElementById(id)?.addEventListener("change", (e) => {
        fn(e.target.value);
        this._refreshIconPreview();
      });
    };
    bindIcon("i-mode", (v) => (this._draft.icon.mode = v));
    bindIcon("i-mdi", (v) => (this._draft.icon.mdi_icon = v.trim()));
    bindIcon("i-fg", (v) => (this._draft.icon.icon_color = v));
    bindIcon("i-bg", (v) => (this._draft.icon.bg_color = v));
    bindIcon("i-radius", (v) => (this._draft.icon.corner_radius_pct = Number(v || 0)));
    bindIcon("i-badge-mdi", (v) => (this._draft.icon.badge_icon = v.trim()));
    bindIcon("i-badge-pos", (v) => (this._draft.icon.badge_position = v));
    bindIcon("i-badge-fg", (v) => (this._draft.icon.badge_color = v));
    bindIcon("i-badge-bg", (v) => (this._draft.icon.badge_bg_color = v));

    sr.getElementById("i-use-dash-icon-btn")?.addEventListener("click", () => {
      const dash = this._dashboards.find(
        (db) => db.url_path === this._draft.content.dashboard_url_path
      );
      const dashIcon = dash?.icon || "mdi:view-dashboard";
      this._draft.icon.mdi_icon = dashIcon;
      this._draft.icon.resolved_dashboard_icon = dashIcon;
      this._render();
      this._refreshIconPreview();
    });

    sr.getElementById("i-upload")?.addEventListener("change", (ev) => {
      const file = ev.target.files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        this._draft.icon.uploaded_image_b64 = String(reader.result || "");
        this._draft.icon.uploaded_mime = file.type || "image/png";
        if (this._draft.icon.mode !== "icon_with_ha_badge") {
          this._draft.icon.mode = "uploaded";
        }
        this._render();
        this._refreshIconPreview();
      };
      reader.readAsDataURL(file);
    });

    bindVal("access-mode", mode => {
      Object.assign(this._draft.access, {
        local_guests: mode === "guest",
        require_admin: mode === "admin",
        allow_all_authenticated: mode === "all",
        allowed_user_ids: [],
      });
      this._render();
      this._renderDevicePreviewCards();
      sr.getElementById("access-mode").focus();
    });
    sr.getElementById("reload-users")?.addEventListener("click", async () => {
      try {
        const result = await this._hass.callWS({ type: "pwa_app_studio/users/list" });
        this._users = result.users || [];
      } catch (err) {
        this._errorMsg = err?.message || "Konten konnten nicht geladen werden.";
      }
      this._render();
      this._renderDevicePreviewCards();
    });
    sr.querySelectorAll(".a-user-cb").forEach((cb) => {
      cb.addEventListener("change", () => {
        const checked = Array.from(sr.querySelectorAll(".a-user-cb"))
          .filter((el) => el.checked)
          .map((el) => el.value);
        this._draft.access.allowed_user_ids = checked;
      });
    });

    sr.getElementById("copy-companion-link")?.addEventListener("click", async () => {
      const url = sr.getElementById("companion-url");
      const status = sr.getElementById("companion-copy-status");
      status.hidden = false;
      try {
        await navigator.clipboard.writeText(url.value);
        status.textContent = "Companion-Link kopiert.";
      } catch {
        sr.getElementById("companion-link-details").open = true;
        url.focus();
        url.select();
        status.textContent = "Der Link ist markiert. Kopiere ihn über das Auswahlmenü.";
      }
    });

    sr.getElementById("install-current-btn")?.addEventListener("click", () =>
      this._handleInstallOnCurrentDevice()
    );
    sr.getElementById("refresh-qr-btn")?.addEventListener("click", () =>
      this._loadQrCode()
    );
  }
}

if (!customElements.get("pwa-app-studio-panel")) {
  customElements.define("pwa-app-studio-panel", PwaAppStudioPanel);
}
