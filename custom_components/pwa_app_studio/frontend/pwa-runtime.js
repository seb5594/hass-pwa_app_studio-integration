/* Standalone PWA runtime hosted at /pwa_app_studio/app/<slug>/ handling SW, IndieAuth PKCE, ACL check, and device install. */

import { chromeInstallLink } from "./pwa-install.js";
import { waitForDeviceApproval } from "./pwa-companion-connect.js";
import { studioLanguage, studioMessage } from "./pwa-studio-i18n.js";

(async () => {
  const root = document.getElementById("pwa-root");
  if (!root) return;

  const slug = root.dataset.slug;
  const appName = root.dataset.name || "Home Assistant PWA";
  const basePath = root.dataset.base;
  const swUrl = root.dataset.swUrl;
  const clientUrl = root.dataset.clientUrl;
  const language = studioLanguage({ config: { language: document.documentElement.lang } });
  const t = (key) => studioMessage(language, key);
  const launch = root.querySelector(".launch");

  const origin = window.location.origin;
  const clientId = `${origin}${clientUrl}`;
  const redirectUri = `${origin}${basePath}`;
  const pkceVerifierKey = `pwa_app_studio_pkce_${slug}`;
  const pkceStateKey = `pwa_app_studio_state_${slug}`;
  const pkceInstallKey = `pwa_app_studio_install_${slug}`;
  const wantsInstall = () => new URLSearchParams(location.search).get("auto_install") === "1";
  const isIos = /iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (/Mac/i.test(navigator.platform) && navigator.maxTouchPoints > 1);
  const isStandalone = () => navigator.standalone === true ||
    ["standalone", "fullscreen", "minimal-ui", "window-controls-overlay"]
      .some(mode => window.matchMedia(`(display-mode: ${mode})`).matches);

  let deferredInstallPrompt = null;
  let installBannerDismissed = false;

  function installInstructions() {
    const ua = navigator.userAgent || "";
    const platform = navigator.userAgentData?.platform || navigator.platform || "";
    const android = /Android/i.test(platform) || /Android/i.test(ua);
    const embedded = android && (/\bwv\b|Home\s?Assistant/i.test(ua) || Boolean(window.externalApp));
    if (!window.isSecureContext) return { hint: t("install_https"), android, embedded };
    if (embedded) return { hint: t("install_webview"), android, embedded };
    if (android) return { hint: t("install_android"), android, embedded };
    if (isIos) {
      return { hint: t("install_ios"), android, embedded };
    }
    const safari = /Mac/i.test(platform) && /Safari/i.test(ua) && !/Chrome|Edg/i.test(ua);
    return { hint: t(safari ? "install_mac" : "install_desktop"), android, embedded };
  }

  window.addEventListener("beforeinstallprompt", (event) => {
    if (!wantsInstall() || installBannerDismissed) return;
    event.preventDefault();
    deferredInstallPrompt = event;
    const button = document.getElementById("pwa-install-btn");
    if (button) button.hidden = false;
  });

  window.addEventListener("appinstalled", () => {
    deferredInstallPrompt = null;
    installBannerDismissed = true;
    document.getElementById("pwa-install-banner")?.remove();
  });

  async function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    try {
      await navigator.serviceWorker.register(swUrl, { scope: basePath });
    } catch (err) {
      console.warn("PWA Web-App Studio SW registration failed:", err);
    }
  }

  function randomString(length = 48) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
    const arr = new Uint8Array(length);
    crypto.getRandomValues(arr);
    return Array.from(arr, (b) => chars[b % chars.length]).join("");
  }

  async function sha256Base64Url(input) {
    const data = new TextEncoder().encode(input);
    const hash = await crypto.subtle.digest("SHA-256", data);
    const bytes = new Uint8Array(hash);
    let str = "";
    for (const b of bytes) str += String.fromCharCode(b);
    return btoa(str).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function readStoredTokens() {
    try {
      const raw = localStorage.getItem("hassTokens");
      if (!raw) return null;
      const tokens = JSON.parse(raw);
      return tokens?.hassUrl?.replace(/\/$/, "") === origin ? tokens : null;
    } catch (_e) {
      return null;
    }
  }

  function saveStoredTokens(tokens) {
    localStorage.setItem("hassTokens", JSON.stringify(tokens));
  }

  function saveNewSession(tokenData) {
    const tokens = {
      hassUrl: origin,
      clientId,
      expires: Date.now() + (tokenData.expires_in || 1800) * 1000,
      access_token: tokenData.access_token,
      refresh_token: tokenData.refresh_token,
      token_type: tokenData.token_type || "Bearer",
      ha_auth_provider: tokenData.ha_auth_provider,
    };
    saveStoredTokens(tokens);
    return tokens;
  }

  async function startOAuthFlow() {
    const state = randomString(24);
    sessionStorage.setItem(pkceStateKey, state);
    if (wantsInstall()) sessionStorage.setItem(pkceInstallKey, "1");
    else sessionStorage.removeItem(pkceInstallKey);

    const authUrl = new URL("/auth/authorize", origin);
    authUrl.searchParams.set("client_id", clientId);
    authUrl.searchParams.set("redirect_uri", redirectUri);
    authUrl.searchParams.set("state", state);

    if (window.crypto?.subtle) {
      const verifier = randomString(64);
      const challenge = await sha256Base64Url(verifier);
      sessionStorage.setItem(pkceVerifierKey, verifier);
      authUrl.searchParams.set("code_challenge", challenge);
      authUrl.searchParams.set("code_challenge_method", "S256");
    }

    window.location.href = authUrl.toString();
  }

  async function exchangeCodeIfPresent() {
    const url = new URL(window.location.href);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state");
    if (!code) return null;

    const expectedState = sessionStorage.getItem(pkceStateKey);
    if (!expectedState || state !== expectedState) {
      window.history.replaceState(null, "", basePath);
      throw new Error("Ungültiger OAuth-State-Parameter.");
    }

    const body = new URLSearchParams();
    body.set("grant_type", "authorization_code");
    body.set("code", code);
    body.set("client_id", clientId);

    const verifier = sessionStorage.getItem(pkceVerifierKey);
    if (verifier) {
      body.set("code_verifier", verifier);
    }

    const resp = await fetch("/auth/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
    if (!resp.ok) {
      throw new Error("OAuth Token-Austausch fehlgeschlagen.");
    }
    const stored = saveNewSession(await resp.json());
    sessionStorage.removeItem(pkceVerifierKey);
    sessionStorage.removeItem(pkceStateKey);
    if (sessionStorage.getItem(pkceInstallKey) === "1") {
      url.searchParams.set("auto_install", "1");
    }
    sessionStorage.removeItem(pkceInstallKey);

    url.searchParams.delete("code");
    url.searchParams.delete("state");
    window.history.replaceState(null, "", url.toString());
    return stored;
  }

  async function refreshAccessToken(tokens) {
    if (!tokens?.refresh_token) return null;
    const body = new URLSearchParams();
    body.set("grant_type", "refresh_token");
    body.set("refresh_token", tokens.refresh_token);
    body.set("client_id", tokens.clientId || clientId);

    const resp = await fetch("/auth/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
    if (!resp.ok) return null;
    const refreshed = await resp.json();
    const updated = {
      ...tokens,
      access_token: refreshed.access_token,
      expires: Date.now() + (refreshed.expires_in || 1800) * 1000,
    };
    saveStoredTokens(updated);
    return updated;
  }

  async function ensureAuthenticatedTokens() {
    let tokens = await exchangeCodeIfPresent();
    if (!tokens) tokens = readStoredTokens();
    if (!tokens?.access_token) {
      return signIn();
    }
    if (tokens.expires && Date.now() > tokens.expires - 60000) {
      const refreshed = await refreshAccessToken(tokens);
      if (refreshed) tokens = refreshed;
    }
    return tokens;
  }

  async function signIn() {
    if (root.dataset.companionPairing !== "true" || !window.isSecureContext) {
      await startOAuthFlow();
      return null;
    }
    return saveNewSession(await waitForDeviceApproval({
      launch, slug, t,
      passwordLogin: startOAuthFlow,
      iosBrowser: isIos && !isStandalone(),
    }));
  }

  function esc(val) {
    return String(val ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderStatusCard(title, message, actionHtml = "") {
    root.innerHTML = `
      <main class="launch">
        <div class="welcome">
          <div class="mark"><img src="${basePath}icon-192.png" alt="" width="76" height="76" /></div>
          <h1>${esc(title)}</h1>
          <p role="status">${message}</p>
          ${actionHtml}
        </div>
      </main>
    `;
  }

  function renderInstallBannerIfWanted() {
    if (!wantsInstall() || installBannerDismissed || document.getElementById("pwa-install-banner")) return;
    if (isStandalone()) return;

    const { hint, android, embedded } = installInstructions();
    const installUrl = new URL(basePath, origin);
    installUrl.searchParams.set("auto_install", "1");
    const chromeUrl = embedded ? chromeInstallLink(installUrl) : "";

    const banner = document.createElement("section");
    banner.id = "pwa-install-banner";
    banner.className = "install-banner";
    banner.setAttribute("aria-label", t("install_help"));
    banner.innerHTML = `
      <div class="install-heading">
        <strong>${esc(t("install_help"))}</strong>
        <button id="pwa-close-banner" aria-label="${esc(t("install_close"))}">✕</button>
      </div>
      <p>${esc(hint)}</p>
      <div class="install-actions">
        <button id="pwa-install-btn" ${deferredInstallPrompt ? "" : "hidden"}>${esc(t("install_native"))}</button>
        ${chromeUrl ? `<a href="${esc(chromeUrl)}">${esc(t("install_open_chrome"))}</a>` : ""}
        ${android ? `<button id="pwa-copy-install-link">${esc(t("browser_copy"))}</button>` : ""}
      </div>
      <input id="pwa-install-url" type="text" aria-label="${esc(t("qr_url"))}" readonly hidden value="${esc(installUrl.href)}" />
      <p id="pwa-install-status" role="status" hidden></p>
    `;
    root.before(banner);

    banner.querySelector("#pwa-close-banner").onclick = () => {
      installBannerDismissed = true;
      banner.remove();
    };
    const status = banner.querySelector("#pwa-install-status");
    const button = banner.querySelector("#pwa-install-btn");
    button.onclick = async () => {
      const prompt = deferredInstallPrompt;
      if (!prompt) return;
      deferredInstallPrompt = null;
      button.hidden = true;
      try {
        await prompt.prompt();
      } catch {
        status.hidden = false;
        status.textContent = t("install_retry_menu");
      }
    };
    const copy = banner.querySelector("#pwa-copy-install-link");
    if (copy) copy.onclick = async () => {
      const input = banner.querySelector("#pwa-install-url");
      status.hidden = false;
      try {
        await navigator.clipboard.writeText(input.value);
        status.textContent = t("browser_copied");
      } catch {
        input.hidden = false;
        input.focus();
        input.select();
        status.textContent = t("browser_selected");
      }
    };
  }

  renderInstallBannerIfWanted();
  void registerServiceWorker();

  try {
    let tokens = await ensureAuthenticatedTokens();
    if (!tokens) return;

    const getRuntime = (tokens) => fetch(`/api/pwa_app_studio/runtime/${encodeURIComponent(slug)}`, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });
    let runtimeResp = await getRuntime(tokens);

    if (runtimeResp.status === 401) {
      const refreshed = await refreshAccessToken(tokens);
      if (refreshed) {
        tokens = refreshed;
        runtimeResp = await getRuntime(tokens);
      }
      if (runtimeResp.status === 401) {
        tokens = await signIn();
        if (!tokens) return;
        runtimeResp = await getRuntime(tokens);
      }
    }

    if (runtimeResp.status === 403) {
      const errJson = await runtimeResp.json().catch(() => ({}));
      renderStatusCard(
        "Zugriff verweigert",
        `${esc(errJson.message || "Keine Berechtigung für diese App.")}<br/><small>Angemeldet als: ${esc(errJson?.user?.name || "Unbekannt")}</small>`,
        `<button id="relogin-btn">Mit anderem Konto anmelden</button>`
      );
      document.getElementById("relogin-btn")?.addEventListener("click", async () => {
        await startOAuthFlow();
      });
      return;
    }

    if (!runtimeResp.ok) {
      throw new Error(`HTTP ${runtimeResp.status}`);
    }

    document.getElementById("launch-status").textContent = "Deine Ansicht wird geladen …";
    renderInstallBannerIfWanted();

    const frame = document.createElement("iframe");
    frame.src = `/pwa-app-studio-runner?app=${encodeURIComponent(slug)}&pwa_shell=1`;
    frame.title = appName;
    frame.inert = true;
    const reveal = () => {
      clearTimeout(timer);
      window.removeEventListener("message", ready);
      frame.inert = false;
      launch?.remove();
    };
    const ready = (event) => {
      if (event.origin === origin && event.source === frame.contentWindow &&
          event.data?.type === "pwa-app-studio:ready" && event.data.slug === slug) reveal();
    };
    const timer = setTimeout(reveal, 12000);
    window.addEventListener("message", ready);
    frame.allow = "fullscreen";
    root.appendChild(frame);
  } catch (err) {
    renderStatusCard(
      "Verbindungsfehler",
      `Die PWA konnte nicht gestartet werden (${esc(err?.message || err)}).`,
      `<button onclick="window.location.reload()">Erneut versuchen</button>`
    );
  }
})();
