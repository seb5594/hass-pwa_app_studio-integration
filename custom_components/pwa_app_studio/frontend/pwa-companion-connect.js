const COMPANION_URL = "homeassistant://navigate/pwa-app-studio-connect";

export function waitForDeviceApproval({ launch, slug, t, passwordLogin, iosBrowser }) {
  const endpoint = `/api/pwa_app_studio/companion/device/${encodeURIComponent(slug)}`;
  const storageKey = `pwa-app-studio-device:${slug}`;
  const status = launch.querySelector("#launch-status");
  const controls = document.createElement("div");
  controls.className = "companion-connect";
  controls.innerHTML = `
    <p data-ios hidden>${t("pairing_ios_install")}</p>
    <button type="button" data-start>${t("pairing_begin")}</button>
    <div data-request hidden>
      <p>${t("pairing_switch")}</p>
      <p><code></code></p>
      <a class="companion-open" href="${COMPANION_URL}">${t("pairing_open")}</a>
      <button type="button" data-copy>${t("pairing_copy_code")}</button>
      <button type="button" data-check>${t("pairing_check")}</button>
    </div>
    <button type="button" data-password>${t("pairing_password")}</button>`;
  status.textContent = t("pairing_sign_in");
  status.after(controls);
  controls.querySelector("[data-ios]").hidden = !iosBrowser;
  const start = controls.querySelector("[data-start]");
  const check = controls.querySelector("[data-check]");
  const copy = controls.querySelector("[data-copy]");
  const password = controls.querySelector("[data-password]");
  const request = controls.querySelector("[data-request]");
  copy.hidden = !navigator.clipboard?.writeText;
  async function post(data) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      return await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        cache: "no-store",
        signal: controller.signal,
        body: JSON.stringify(data),
      });
    } finally {
      clearTimeout(timeout);
    }
  }

  return new Promise((resolve) => {
    let pairing = null;
    let timer;
    let checking = false;
    let leaving = false;
    try {
      pairing = JSON.parse(sessionStorage.getItem(storageKey));
    } catch {
      // The current page can still pair if storage is unavailable.
    }

    const remember = () => {
      try {
        if (pairing) sessionStorage.setItem(storageKey, JSON.stringify(pairing));
        else sessionStorage.removeItem(storageKey);
      } catch {
        // The current page can still pair if storage is unavailable.
      }
    };
    const showCode = () => {
      start.hidden = Boolean(pairing);
      request.hidden = !pairing;
      if (pairing) {
        request.querySelector("code").textContent = pairing.code.match(/.{1,4}/g).join(" ");
        status.textContent = t("pairing_pending");
      }
    };
    const expire = () => {
      pairing = null;
      remember();
      showCode();
      status.textContent = t("pairing_expired");
      start.textContent = t("pairing_retry");
    };
    async function poll() {
      clearTimeout(timer);
      if (!pairing || checking || leaving || document.hidden) return;
      if (Date.now() >= pairing.deadline) {
        expire();
        return;
      }
      checking = true;
      check.disabled = true;
      password.disabled = true;
      try {
        const response = await post({ code: pairing.code, secret: pairing.secret });
        if (response.status === 202) {
          status.textContent = t("pairing_pending");
        } else if (response.status === 404 || response.status === 403) {
          expire();
        } else if (response.ok) {
          const tokens = await response.json();
          pairing = null;
          remember();
          document.removeEventListener("visibilitychange", poll);
          controls.remove();
          resolve(tokens);
        } else {
          throw new Error("Pairing request failed");
        }
      } catch {
        status.textContent = t("pairing_failed");
      } finally {
        checking = false;
        check.disabled = false;
        password.disabled = false;
        if (pairing && !document.hidden) timer = setTimeout(poll, 3000);
      }
    }
    start.onclick = async () => {
      start.disabled = true;
      password.disabled = true;
      try {
        const response = await post({});
        if (!response.ok) throw new Error("Could not start pairing");
        const { code, secret, expires_in } = await response.json();
        pairing = { code, secret, deadline: Date.now() + expires_in * 1000 };
        remember();
        showCode();
        controls.querySelector("a").focus();
        timer = setTimeout(poll, 3000);
      } catch {
        status.textContent = t("pairing_failed");
      } finally {
        start.disabled = false;
        password.disabled = false;
      }
    };
    password.onclick = async () => {
      leaving = true;
      clearTimeout(timer);
      try {
        await passwordLogin();
        pairing = null;
        remember();
      } catch {
        leaving = false;
        status.textContent = t("pairing_failed");
        if (pairing) timer = setTimeout(poll, 3000);
      }
    };
    check.onclick = poll;
    copy.onclick = async () => {
      try {
        await navigator.clipboard.writeText(pairing.code);
        status.textContent = t("pairing_copied");
      } catch {
        status.textContent = t("pairing_switch");
      }
    };
    document.addEventListener("visibilitychange", poll);
    showCode();
    if (pairing) void poll();
  });
}
