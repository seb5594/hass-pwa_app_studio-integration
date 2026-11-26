<!-- header:begin (generated from project metadata) -->
<h1 align="center">PWA Web-App Studio</h1>

<p align="center">
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=seb5594&amp;repository=hass-pwa_app_studio-integration&amp;category=integration"><img src="https://img.shields.io/static/v1?label=HACS%20%C2%B7%20Marketplace&amp;message=Add%20integration&amp;color=41BDF5&amp;logo=homeassistantcommunitystore&amp;logoColor=white&amp;style=for-the-badge" alt="HACS · Marketplace" height="28"></a>
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration/actions/workflows/compat.yml"><img src="https://img.shields.io/static/v1?label=home%20assistant&amp;message=%E2%89%A5%202021.12.0&amp;color=1877A5&amp;style=for-the-badge" alt="home assistant" height="28"></a><br>
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration/releases/tag/2026.11.26.2"><img src="https://img.shields.io/static/v1?label=integration%20version&amp;message=2026.11.26.2&amp;color=1877A5&amp;style=for-the-badge" alt="integration version" height="28"></a>
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration/releases"><img src="https://img.shields.io/github/downloads/seb5594/hass-pwa_app_studio-integration/2026.11.26.2/total?label=downloads&amp;color=1877A5&amp;style=for-the-badge" alt="downloads" height="28"></a><br>
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/seb5594/hass-pwa_app_studio-integration/ci.yml?branch=main&amp;label=checks&amp;style=flat" alt="checks" height="20"></a>
  <img src="https://img.shields.io/static/v1?label=tests&amp;message=2%20passed&amp;color=2F855A&amp;style=flat" alt="tests" height="20">
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration/issues"><img src="https://img.shields.io/github/issues/seb5594/hass-pwa_app_studio-integration?label=issues&amp;style=flat" alt="issues" height="20"></a><br>
  <a href="https://paypal.me/seb5594"><img src="https://img.shields.io/static/v1?label=Support&amp;message=PayPal&amp;color=0070BA&amp;logo=paypal&amp;logoColor=white&amp;style=for-the-badge" alt="PayPal" height="24"></a>
  <a href="https://buymeacoffee.com/seb5594"><img src="https://raw.githubusercontent.com/seb5594/Home-Assistant-Apps/473dc258f963096745aac327df54950eb9b59066/.github/assets/support-beer.svg" alt="Buy me a beer" height="24"></a><br>
  <a href="https://github.com/seb5594/hass-pwa_app_studio-integration#license"><img src="https://img.shields.io/github/license/seb5594/hass-pwa_app_studio-integration?label=license&amp;style=flat" alt="license" height="20"></a>
</p>
<!-- header:end -->

**🇬🇧 English** · [🇩🇪 Deutsch](README.de.md)

PWA Web-App Studio is a custom Home Assistant integration that lets administrators turn Lovelace dashboards or selected cards into installable web apps. Each app has its own URL, icon, and access settings.

## Try the first draft

1. Copy `custom_components/pwa_app_studio/` into the `custom_components/` directory of a test Home Assistant installation.
2. Restart Home Assistant and add **PWA Web-App Studio** under **Settings > Devices & services > Add integration**.
3. Open **PWA Web-App Studio** from the sidebar, choose a dashboard or add cards, then save the app.
4. Open the app via its QR code or install link on a device that can reach Home Assistant over HTTPS.

The app uses the signed-in Home Assistant account. Dashboard access still depends on that account's Home Assistant permissions. Offline caching covers the app shell and assets. Lovelace content needs a connection to Home Assistant.

## Launch and sharing

The five-step designer previews the app’s launch screen and offers three motion styles. Choose **Guests on the home network** to share an app with selected local-only, non-admin Home Assistant accounts through the internal URL. The companion link opens the app in the active Home Assistant session. A standalone installation reuses the session available to its browser context and signs in through Home Assistant when needed.

Minimum Home Assistant Core version: **2021.12.0**. Core versions before 2022.11 offer a button card in place of the Tile preset. Installing a PWA needs a current browser.

[Architectural review (German)](docs/architekturpruefung.md)

<!-- support:begin (generated, shared text) -->
## Say thanks

All my projects are built in my spare time, just for the fun of it. Still, they take a lot of time and care, and many of the smart home gadgets I buy end up here because I want to make them cloud-free and smart-home ready. Every bit of support means a lot to me.

If my work helped you or turned out to be useful, show your appreciation with a hot drink for my next sleepless night.

[![PayPal](https://img.shields.io/static/v1?label=Support&message=PayPal&color=0070BA&logo=paypal&logoColor=white&style=for-the-badge)](https://paypal.me/seb5594) [![Buy me a beer](https://raw.githubusercontent.com/seb5594/Home-Assistant-Apps/473dc258f963096745aac327df54950eb9b59066/.github/assets/support-beer.svg)](https://buymeacoffee.com/seb5594)
<!-- support:end -->

<!-- license:begin (generated from the license file) -->
## License

[![license](https://img.shields.io/static/v1?label=license&message=Apache-2.0&color=5B6770&style=flat)](LICENSE)

Published under the [Apache License 2.0](LICENSE).
<!-- license:end -->
