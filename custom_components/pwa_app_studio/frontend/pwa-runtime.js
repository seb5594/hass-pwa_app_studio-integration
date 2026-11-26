/* Standalone PWA runtime hosted at /pwa_app_studio/app/<slug>/ handling SW, IndieAuth PKCE, ACL check, and device install. */

(async () => {
  const root = document.getElementById("pwa-root");
  if (!root) return;

  const slug = root.dataset.slug;
  const appName = root.dataset.name || "Home Assistant PWA";
  const basePath = root.dataset.base;
  const swUrl = root.dataset.swUrl;
  const clientUrl = root.dataset.clientUrl;
  const themeColor = root.dataset.theme || "#03a9f4";
  const launch = root.querySelector(".launch");

  const origin = window.location.origin;
  const clientId = `${origin}${clientUrl}`;
  const redirectUri = `${origin}${basePath}`;
  const pkceVerifierKey = `pwa_app_studio_pkce_${slug}`;
  const pkceStateKey = `pwa_app_studio_state_${slug}`;

  let deferredInstallPrompt = null;

  function detectPlatform() {
    const uaData = navigator.userAgentData;
    const ua = navigator.userAgent || "";
    const platform = uaData?.platform || navigator.platform || "";
    const isTouchMac = /Mac/i.test(platform) && navigator.maxTouchPoints > 1;
    const isIos = /iPhone|iPad|iPod/i.test(ua) || isTouchMac;
    const isAndroid = /Android/i.test(ua) || /Android/i.test(platform);
    const isStandalone =
      window.matchMedia?.("(display-mode: standalone)").matches ||
      window.navigator.standalone === true;
    const isEdge =
      Boolean(uaData?.brands?.some((b) => /Edge/i.test(b.brand))) || /Edg/i.test(ua);
    const isSafari = /Safari/i.test(ua) && !/Chrome|CriOS|FxiOS|Edg/i.test(ua);

    if (isIos) {
      return {
        key: isTouchMac || /iPad/i.test(ua) ? "ipados" : "ios",
        label: isTouchMac || /iPad/i.test(ua) ? "iPadOS (Safari)" : "iOS (Safari)",
        isStandalone,
        supportsNativePrompt: false,
        instructions:
          "Tippe unten/oben auf das Teilen-Symbol (Quadrat mit Pfeil) und wähle 'Zum Home-Bildschirm'.",
      };
    }
    if (isAndroid) {
      return {
        key: "android",
        label: isEdge ? "Android (Edge)" : "Android (Chrome / Chromium)",
        isStandalone,
        supportsNativePrompt: true,
        instructions:
          "Tippe auf 'Jetzt installieren' oder im Browser-Menü auf 'App installieren'.",
      };
    }
    if (/Mac/i.test(platform) && isSafari) {
      return {
        key: "macos_safari",
        label: "macOS (Safari)",
        isStandalone,
        supportsNativePrompt: false,
        instructions: "Wähle im Safari-Menü 'Ablage → Zum Dock hinzufügen'.",
      };
    }
    return {
      key: "desktop_chromium",
      label: isEdge ? `Desktop (${platform || "Edge"})` : `Desktop (${platform || "Chrome"})`,
      isStandalone,
      supportsNativePrompt: true,
      instructions:
        "Klicke auf 'Jetzt installieren' oder auf das Install-Symbol in der Adressleiste.",
    };
  }

  window.addEventListener("beforeinstallprompt", (ev) => {
    ev.preventDefault();
    deferredInstallPrompt = ev;
    const btn = document.getElementById("pwa-install-btn");
    if (btn) {
      btn.disabled = false;
      btn.textContent = `Auf ${detectPlatform().label} installieren`;
    }
  });

  window.addEventListener("appinstalled", () => {
    deferredInstallPrompt = null;
    const banner = document.getElementById("pwa-install-banner");
    if (banner) banner.remove();
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

  async function startOAuthFlow() {
    const state = randomString(24);
    sessionStorage.setItem(pkceStateKey, state);

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
    const tokenData = await resp.json();
    const stored = {
      hassUrl: origin,
      clientId,
      expires: Date.now() + (tokenData.expires_in || 1800) * 1000,
      access_token: tokenData.access_token,
      refresh_token: tokenData.refresh_token,
      token_type: tokenData.token_type || "Bearer",
      ha_auth_provider: tokenData.ha_auth_provider,
    };
    saveStoredTokens(stored);
    sessionStorage.removeItem(pkceVerifierKey);
    sessionStorage.removeItem(pkceStateKey);

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
      await startOAuthFlow();
      return null;
    }
    if (tokens.expires && Date.now() > tokens.expires - 60000) {
      const refreshed = await refreshAccessToken(tokens);
      if (refreshed) tokens = refreshed;
    }
    return tokens;
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
    const plat = detectPlatform();
    const params = new URLSearchParams(window.location.search);
    const wantsInstall = params.get("auto_install") === "1";
    if (plat.isStandalone || !wantsInstall) return;

    const banner = document.createElement("div");
    banner.id = "pwa-install-banner";
    banner.style.cssText = `
      display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;
      padding:10px 14px;background:${themeColor};color:#fff;font-size:13px;z-index:20;
    `;
    banner.innerHTML = `
      <div>
        <strong>${esc(appName)}</strong> — Erkanntes Gerät: <b>${esc(plat.label)}</b><br/>
        <span style="opacity:0.95">${esc(plat.instructions)}</span>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        ${
          plat.supportsNativePrompt
            ? `<button id="pwa-install-btn" style="background:#111827;color:#fff;border:none;border-radius:8px;padding:8px 12px;cursor:pointer;font-weight:600;">
                 ${deferredInstallPrompt ? `Auf ${esc(plat.label)} installieren` : "Installationsdialog prüfen"}
               </button>`
            : ""
        }
        <button id="pwa-close-banner" style="background:rgba(255,255,255,0.2);color:#fff;border:none;border-radius:8px;padding:8px 10px;cursor:pointer;">✕</button>
      </div>
    `;
    root.prepend(banner);

    document.getElementById("pwa-close-banner")?.addEventListener("click", () => banner.remove());
    document.getElementById("pwa-install-btn")?.addEventListener("click", async () => {
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        await deferredInstallPrompt.userChoice;
        deferredInstallPrompt = null;
      } else {
        alert(plat.instructions);
      }
    });
  }

  void registerServiceWorker();

  try {
    let tokens = await ensureAuthenticatedTokens();
    if (!tokens) return;

    let runtimeResp = await fetch(`/api/pwa_app_studio/runtime/${encodeURIComponent(slug)}`, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });

    if (runtimeResp.status === 401) {
      const refreshed = await refreshAccessToken(tokens);
      if (refreshed) {
        tokens = refreshed;
        runtimeResp = await fetch(`/api/pwa_app_studio/runtime/${encodeURIComponent(slug)}`, {
          headers: { Authorization: `Bearer ${tokens.access_token}` },
        });
      }
      if (runtimeResp.status === 401) {
        await startOAuthFlow();
        return;
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
