export function isAndroidWebView() {
  const ua = navigator.userAgent || "";
  const platform = navigator.userAgentData?.platform || navigator.platform || "";
  return /Android/i.test(`${platform} ${ua}`) &&
    (/\bwv\b|Home\s?Assistant/i.test(ua) || Boolean(window.externalApp || window.externalAppV2));
}

/* Android resolves this HTTP(S) intent to the user's browser. */
export function androidBrowserLink(url) {
  const target = new URL(url);
  if (!["https:", "http:"].includes(target.protocol) || target.username || target.password) return "";
  target.hash = "";
  const scheme = target.protocol.slice(0, -1);
  const fallback = encodeURIComponent(target.href);
  return `intent://${target.host}${target.pathname}${target.search}#Intent;scheme=${scheme};action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;S.browser_fallback_url=${fallback};end`;
}
