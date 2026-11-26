import { studioLanguage, studioMessage } from "./pwa-studio-i18n.js";

class PwaAppStudioConnectPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  set hass(value) {
    this._hass = value;
    if (!this.shadowRoot.firstChild && value) this._render();
  }

  _render() {
    const t = (key, values) => studioMessage(studioLanguage(this._hass), key, values);
    const sr = this.shadowRoot;
    sr.innerHTML = `
      <style>
        :host { display:block; height:100%; overflow:auto; box-sizing:border-box; color:var(--primary-text-color); }
        main { max-width:32rem; margin:auto; padding:24px 20px max(24px,env(safe-area-inset-bottom)); }
        h1 { margin-top:0; font-size:clamp(1.65rem,5vw,2.25rem); letter-spacing:-.03em; }
        form, section { border:1px solid var(--divider-color); border-radius:22px; padding:20px; background:var(--card-background-color); }
        p { overflow-wrap:anywhere; line-height:1.5; }
        label { display:grid; gap:8px; }
        input { width:100%; min-width:0; min-height:48px; box-sizing:border-box; font:1rem ui-monospace, monospace;
          color:inherit; background:var(--primary-background-color); border:1px solid var(--divider-color);
          border-radius:12px; padding:10px; text-transform:uppercase; letter-spacing:.08em; }
        button { min-height:44px; margin-top:12px; padding:8px 16px; border-radius:24px; border:1px solid var(--divider-color);
          background:var(--card-background-color); color:inherit; font:inherit; cursor:pointer; }
        button.primary { background:#2058cf; color:white; border-color:#2058cf; }
        button:disabled { opacity:.6; }
        [hidden] { display:none !important; }
      </style>
      <main>
        <h1>${t("pairing_panel_title")}</h1>
        <form>
          <p>${t("pairing_panel_intro")}</p>
          <label>${t("pairing_code")}
            <input name="code" required maxlength="20" autocomplete="off" autocapitalize="characters" spellcheck="false"
              placeholder="ABCD EFGH JKLM">
          </label>
          <button type="submit" class="primary">${t("pairing_lookup")}</button>
        </form>
        <section hidden>
          <p id="request"></p>
          <p>${t("pairing_scope")}</p>
          <button id="confirm" class="primary">${t("pairing_confirm")}</button>
          <button id="back">${t("pairing_back")}</button>
        </section>
        <p id="status" role="status"></p>
      </main>`;
    const form = sr.querySelector("form");
    const input = form.elements.code;
    const submit = form.querySelector("button");
    const review = sr.querySelector("section");
    const status = sr.getElementById("status");
    const confirm = sr.getElementById("confirm");
    if (!window.isSecureContext) {
      form.hidden = true;
      status.textContent = t("pairing_secure");
      return;
    }
    let code;
    const request = (confirm = false) => this._hass.callApi("POST", "pwa_app_studio/companion/approve", { code, confirm });
    form.onsubmit = async (event) => {
      event.preventDefault();
      code = input.value.toUpperCase().replace(/[\s-]/g, "");
      status.textContent = "";
      submit.disabled = true;
      try {
        const { name, origin, account } = await request();
        sr.getElementById("request").textContent = t("pairing_review", { app: name, origin, user: account });
        form.hidden = true;
        review.hidden = false;
        confirm.focus();
      } catch {
        status.textContent = t("pairing_invalid");
      } finally {
        submit.disabled = false;
      }
    };
    sr.getElementById("back").onclick = () => {
      review.hidden = true;
      form.hidden = false;
      status.textContent = "";
      input.focus();
    };
    confirm.onclick = async () => {
      confirm.disabled = true;
      try {
        await request(true);
        review.hidden = true;
        input.value = "";
        status.textContent = t("pairing_done");
      } catch {
        status.textContent = t("pairing_invalid");
      } finally {
        confirm.disabled = false;
      }
    };
  }
}

customElements.define("pwa-app-studio-connect-panel", PwaAppStudioConnectPanel);
