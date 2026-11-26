# Changelog

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
