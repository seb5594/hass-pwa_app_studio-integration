export function isAndroidDevice() {
  return /Android/i.test(`${navigator.userAgentData?.platform || navigator.platform} ${navigator.userAgent}`);
}

export function isCompanionWebView() {
  return Boolean(window.externalApp || window.externalAppV2 || window.webkit?.messageHandlers?.externalBus) ||
    new URLSearchParams(location.search).get("external_auth") === "1" ||
    /Home\s?Assistant/i.test(navigator.userAgent || "");
}

export function isAndroidWebView() {
  return isAndroidDevice() && (isCompanionWebView() || /\bwv\b/i.test(navigator.userAgent || ""));
}

/* Android resolves this HTTP(S) intent to the user's browser. */
export function androidBrowserLink(url, useChrome = false) {
  const target = new URL(url);
  if (!["https:", "http:"].includes(target.protocol) || target.username || target.password) return "";
  target.hash = "";
  const scheme = target.protocol.slice(0, -1);
  const fallback = encodeURIComponent(target.href);
  const app = useChrome ? "package=com.android.chrome;" : "";
  return `intent://${target.host}${target.pathname}${target.search}#Intent;scheme=${scheme};action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;${app}S.browser_fallback_url=${fallback};end`;
}

export function companionAppLink(path) {
  if (!isAndroidDevice() || isCompanionWebView()) return `homeassistant://navigate${path}`;
  return `intent://navigate${path}#Intent;scheme=homeassistant;action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;package=io.homeassistant.companion.android;end`;
}
