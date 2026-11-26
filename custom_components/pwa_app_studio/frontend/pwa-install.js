/* Build the Android Chrome handoff from an HTTP(S) URL. */
export function chromeBrowserLink(url) {
  const target = new URL(url);
  if (!["https:", "http:"].includes(target.protocol) || target.username || target.password) return "";
  target.hash = "";
  const scheme = target.protocol.slice(0, -1);
  const fallback = encodeURIComponent(target.href);
  return `intent://${target.host}${target.pathname}${target.search}#Intent;scheme=${scheme};action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;package=com.android.chrome;S.browser_fallback_url=${fallback};end`;
}
