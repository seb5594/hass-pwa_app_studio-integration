# Changelog

## 2026.11.26.91

- Add a visual Lovelace card editor, regional translations and localized setup guides.
- Open the Studio from integration options and add optional Sidebar Panel and Open PWA Designer entities.
- Set a display version per web app and offer a reload when an open app has a newer revision.

## 2026.11.26.90

- Recover HACS update discovery where the GitHub release list sorts single-digit builds before builds 10–12.
- Keep the web app on the sign-in chooser until the user selects a sign-in method.
- Navigate directly inside the Companion App and show clickable browser choices when system sharing is unavailable.

## 2026.11.26.12

- Open the matching device request in the Companion App and complete sign-in in the browser tab that started the request.
- Use the default browser for Android sharing and installation handoffs.

## 2026.11.26.11

- Open the native share dialog where supported. On Android WebViews, hand the web app link to a share page in Chrome.

## 2026.11.26.10

- Let users approve a separate web-app session from an already signed-in Companion App on Android or iOS. Site owners can enable this per web app.

## 2026.11.26.9

- Add Aurora, Orbit, Light sweep and Soft entrance launch animations with an instant preview and replay in the designer.

## 2026.11.26.8

- Use a versioned frontend directory with ordinary module imports for the Home Assistant panel loader.

## 2026.11.26.7

- Load frontend dependencies from the same release so stale translations cannot break the Share step.
- Keep the normal browser link and installation available while a QR code loads or if its request fails.

## 2026.11.26.6

- Open Android installation links in Chrome and show the native install button when the browser offers it.
- Serve the adaptive Android app icon from its own route so the manifest can load it.
- Keep installation guidance after sign-in and add share and copy buttons for the browser link.
- Render larger, scalable black-and-white QR codes with a four-module quiet zone.

## 2026.11.26.5

- Show the designer in English by default and automatically switch to German for German Home Assistant servers.

## 2026.11.26.4

- Give the designer and new web apps a blue accent, with each app's selected color applied to its view navigation.

## 2026.11.26.3

- Give the studio designer its own logo and make the Companion link easy to copy.
- Document Companion sign-in, guest setup, and an in-app dashboard button.

## 2026.11.26.2

- Support Home Assistant Core 2021.12.0 and newer, including older Python, static routes, Lovelace dashboards and icon libraries.
- Use a button card on Core versions before the Tile card was introduced. Check local-only access explicitly for older WebSocket sessions.
- Test integration setup, the designer button, sidebar option reloading and runtime authorization across Core versions.

## 2026.11.26.1

- Guide setup through five steps, add per-app launch animations with a live sample and credit the developer in every installed app.
- Open an app in the Home Assistant Companion App using its active session.
- Classify the integration under Local services and validate the manifest with hassfest.
- Share guest apps with selected local-only Home Assistant accounts via the internal URL.
- Isolate offline caches, check OAuth callback state and publish app changes only after storage succeeds.

## 2026.11.26

- Rename the designer to PWA Web-App Studio, simplify setup and adapt navigation and preview for phones.

## 1.0.0

- Import the first PWA App Studio implementation as `pwa_app_studio`, with an admin designer, Lovelace app runtime, icons and QR distribution.
