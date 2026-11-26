# Architekturprüfung PWA Web-App Studio

Stand 2026.11.26.1

| Bereich | Ablauf und Befund |
| --- | --- |
| Einrichtung | Home Assistant registriert einen Admin-Designer und eine ausgeblendete Laufzeitansicht. Der Designer und neue Entwürfe verwenden Blau als Akzentfarbe. Jede App kann eine eigene Akzentfarbe erhalten. Fünf Schritte führen von Namen und Farben über Inhalt und Symbol bis zur Freigabe. |
| Domäne und Speicherung | Manifest, Inhalt, Icon und Freigabe werden als App-Modell abgelegt. Der Anwendungsdienst serialisiert Schreiboperationen. Geänderte Objekte werden erst nach erfolgreichem Speichern aktiv. Vorhandene Apps laden mit bisherigen Berechtigungen und einem Standard-Startstil. |
| Veröffentlichung | App-Hülle, Installationsmanifest und Icon sind öffentlich adressierbar. Interna wie Karten und Benutzerliste laufen über die angemeldeten Schnittstellen. Der Release-Prozess packt die Integration als HACS-ZIP und setzt stabile Releases explizit als Latest. |
| Öffnen | Die Hülle zeigt auf dem ersten Bild App-Symbol, Startstil und Versionsfooter. Die Laufzeit prüft die bestehende Sitzung und öffnet den Home-Assistant-Runner. Der Runner prüft seine Freigabe über die WebSocket-Verbindung und lädt die Karten mit Home Assistants Lovelace-Helpern. Die Companion-Verknüpfung öffnet diesen Runner direkt in der vorhandenen Sitzung. Beim Direktstart lädt das Studio zuerst Home Assistants Lovelace-Modul, damit auch ein frisch geöffnetes Browserfenster Karten darstellen kann. |
| Zugriff | HTTP und WebSocket wenden dieselbe App-Freigabe an. Im Gastmodus sind Administratoren und ausdrücklich gewählte Konten mit „Nur lokaler Zugriff“ berechtigt. Home Assistant prüft die lokale Verbindung. Der QR-Code verteilt die interne URL. Eine ausgewählte, später entfernte Dashboard-Ansicht führt zu einer Meldung. |
| Offline | Der Service Worker speichert nur explizit aufgeführte öffentliche Dateien. App- und Integrationsversion trennen die Cache-Stände. OAuth-Callbacks, Tokens und Karten bleiben außerhalb des Offline-Caches. |

## Offene Grenzen

- Heimnetzfreigabe hängt von Home Assistants Netzwerkerkennung und der korrekten Proxy-Konfiguration ab. Ein Gastkonto hat die normalen, außerhalb der App zugewiesenen Home-Assistant-Rechte. Die PWA bildet keine zusätzliche Sandbox für Entitäten oder benutzerdefinierte Karten.
- Apps teilen sich die Origin ihrer Home-Assistant-Instanz. Die Anmeldung ist an den jeweiligen Browser- oder App-Kontext und die aufgerufene Adresse gebunden. Installierbarkeit und Offline-Hülle hängen von einem sicheren Kontext und der Browserunterstützung ab.
- Der URL-Pfad bestimmt Gültigkeitsbereich und Identität der installierten PWA. Eine nachträgliche Änderung des Pfads erfordert einen neuen Link und ggf. eine Neuinstallation.
- Der Direktstart hängt vom Frontend-Router von Home Assistant ab. Der Browser-Test deckt das Laden einer nativen Karte ab. Karten von Drittanbietern und die Darstellung in Android- und iOS-Companion-Versionen erfordern Gerätetests, wenn eine App zur Nutzung verteilt wird.
