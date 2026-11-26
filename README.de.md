# PWA Web-App Studio

[English](README.md) | **Deutsch**

Mit PWA Web-App Studio erstellen Administratoren installierbare Web-Apps aus Lovelace-Dashboards oder ausgewählten Karten. Jede App hat eine eigene URL, ein Icon und eigene Freigaben.

## Ersten Entwurf ausprobieren

1. Kopiere `custom_components/pwa_app_studio/` in den Ordner `custom_components/` einer Home-Assistant-Testinstallation.
2. Starte Home Assistant neu und füge **PWA Web-App Studio** unter **Einstellungen > Geräte & Dienste > Integration hinzufügen** hinzu.
3. Öffne **PWA Web-App Studio** in der Seitenleiste, wähle ein Dashboard oder füge Karten hinzu und speichere die App.
4. Öffne den Installationslink oder QR-Code auf einem Gerät, das Home Assistant über HTTPS erreicht.

Die App verwendet das angemeldete Home-Assistant-Konto. Für ein Dashboard gelten weiterhin dessen Berechtigungen in Home Assistant. Der Offline-Cache speichert die App-Hülle und statische Dateien. Lovelace-Inhalte brauchen eine Verbindung zu Home Assistant.
