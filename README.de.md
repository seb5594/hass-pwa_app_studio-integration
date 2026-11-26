# PWA Web-App Studio

<img src="custom_components/pwa_app_studio/frontend/studio-logo.png" width="96" height="96" alt="Logo von PWA Web-App Studio" />

[🇬🇧 English](README.md) · **🇩🇪 Deutsch**

Du willst dein Küchen-Dashboard aufs Wandtablet holen, den Garten vom Handy aus im Blick behalten oder Besuchern ein paar Bedienelemente freigeben? Mit PWA Web-App Studio machst du aus einem Home-Assistant-Dashboard oder aus einzelnen Lovelace-Karten eine Web-App. Jede App bekommt einen eigenen Link, ein eigenes Symbol, eigene Farben und eine eigene Freigabe.

## Installation

Du brauchst **Home Assistant Core ab 2021.12.0** und ein Administratorkonto für den Designer. Welche Karten es gibt, hängt von deiner Home-Assistant-Version ab. Auf älteren Installationen bietet das Studio zum Beispiel eine Schaltflächenkarte anstelle der Tile-Karte an.

### Marketplace oder HACS

1. Öffne ab Home Assistant 2026.11 **Einstellungen → Marketplace**. Auf früheren Versionen öffnest du **HACS**, sofern es installiert ist.
2. Suche nach **PWA Web-App Studio** oder nutze das Badge **HACS · Marketplace** in der englischen README. Fehlt das Projekt in der Suche, füge `https://github.com/seb5594/hass-pwa_app_studio-integration` im Marketplace über **Über Link hinzufügen** (*Add from link*) ein. In HACS findest du die Option unter **Benutzerdefinierte Repositories**. Verbinde im Marketplace bei Nachfrage dein GitHub-Konto und wähle bei einer Typabfrage **Integration**. [Hilfe zum Marketplace](https://www.home-assistant.io/integrations/marketplace/#custom-repositories) · [Benutzerdefinierte Repositories in HACS](https://hacs.xyz/docs/faq/custom_repositories/)
3. Tippe im Marketplace auf **Installieren** und fülle das Einrichtungsformular aus. In HACS lädst du die Integration herunter, startest Home Assistant neu und wählst unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** das **PWA Web-App Studio** aus.

### Aus der ZIP-Datei installieren

1. Lade `pwa_app_studio.zip` aus dem [aktuellen Release](https://github.com/seb5594/hass-pwa_app_studio-integration/releases/latest) herunter.
2. Entpacke den Inhalt in `custom_components/pwa_app_studio/` im Konfigurationsordner von Home Assistant. Die Manifest-Datei liegt danach unter `custom_components/pwa_app_studio/manifest.json`.
3. Starte Home Assistant neu und füge **PWA Web-App Studio** unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** hinzu.

Lass die Seitenleistenoption eingeschaltet, wenn du den Designer schnell erreichen möchtest. Du erreichst ihn auch direkt über `/pwa-app-studio` auf deiner Home-Assistant-Instanz.

## Deine erste App erstellen

Öffne **PWA Web-App Studio** und klicke auf **+ Neue PWA**. Stellst du unter **Einstellungen → System → Allgemein** Deutsch als Systemsprache ein, erscheint der Designer automatisch auf Deutsch. Sonst verwendet er Englisch. Bei älteren Servern ohne eigene Systemsprache zählt die Sprache der Home-Assistant-Oberfläche.

1. **App**. Gib der App einen Namen und einen Kurznamen für den Startbildschirm. Wähle Akzent- und Hintergrundfarbe. Neue Apps starten mit Blau (`#2563EB`). Unter **Animation beim Öffnen** siehst du jeden neu gewählten Stil direkt mit deinem Symbol und deinen Farben. In der Vorschau kannst du die Animation erneut abspielen. Mit **Ruhiges Standbild** schaltest du die Bewegung für die App aus.
2. **Inhalt**. Wähle ein Dashboard und bei Bedarf eine bestimmte Ansicht. Für eine kleinere App stellst du einzelne Karten zusammen und legst ihr Layout fest.
3. **Symbol**. Verwende das Home-Assistant- oder Dashboard-Symbol, wähle ein MDI-Symbol oder lade ein eigenes Bild hoch. In der Vorschau kannst du zwischen Smartphone, Tablet und Computer wechseln.
4. **Zugriff**. Wähle, wer die App öffnen darf. Du kannst sie für alle angemeldeten Konten, für ausgewählte Personen, für Gäste im Heimnetz oder nur für Administratoren freigeben. Klicke auf **Speichern**.
5. **Teilen**. Öffne die App in der Companion-App, kopiere den Link oder nutze den QR-Code für die Browser-Version.

Die App verwendet die Home-Assistant-Rechte des angemeldeten Kontos. Berücksichtige das bei der Wahl des Dashboards, wenn du die App weitergibst.

## In der Companion-App anmelden und die erstellte App öffnen

1. Öffne auf dem Handy die offizielle **Home Assistant**-App. Wenn du das Dashboard deiner Instanz bereits siehst, bist du angemeldet. Andernfalls wähle **Mit meinem Home-Assistant-Server verbinden** oder bei einer bestehenden Einrichtung **Einstellungen → Companion-App → Server hinzufügen**. Wähle deinen Server oder gib die Adresse ein und melde dich direkt in der App an. [Einrichtung der Companion-App](https://companion.home-assistant.io/docs/getting_started/#step-by-step-setup)
2. Öffne die gespeicherte App im Studio und tippe unter **Teilen** auf **In Home Assistant öffnen**. Wenn du am Computer sitzt, wähle **Companion-Link kopieren** und schicke den Link ans Handy.
3. Tippe auf den Link und wähle bei Nachfrage den richtigen Server. Die Ansicht öffnet sich mit der aktiven Sitzung deiner Companion-App. [Navigationslinks für Android und iOS](https://companion.home-assistant.io/docs/integrations/url-handler/#navigate)

### Eine Schaltfläche im Dashboard anlegen

Du willst einen festen Platz zum Öffnen der App? Kopiere unter **Teilen → Link und Dashboard-Pfad anzeigen** den Dashboard-Pfad. Füge auf einem Dashboard, das das Konto öffnen darf, eine Schaltflächenkarte hinzu. Wähle **Navigieren** als Tipp-Aktion und füge den Pfad ein. Für eine App mit dem URL-Namen `mein-garten` sieht das Beispiel so aus. [Dashboard-Aktionen in Home Assistant](https://www.home-assistant.io/dashboards/actions/)

```yaml
type: button
name: Mein Garten öffnen
icon: mdi:cellphone
tap_action:
  action: navigate
  navigation_path: /pwa-app-studio-runner/mein-garten
```

## Für Gäste im Heimnetz freigeben

1. Lege unter **Einstellungen → Personen → Benutzer** ein Konto an. Schalte **Nur lokaler Zugriff** ein und lass **Administrator** ausgeschaltet. [Benutzerkonten in Home Assistant](https://www.home-assistant.io/docs/configuration/user-configuration/#about-persons-and-users)
2. Wähle im Studio **Zugriff → Gäste im Heimnetz**, markiere das Gastkonto und speichere. Wenn das Studio beim Anlegen des Kontos schon geöffnet war, verwende **Konten neu laden**.
3. Der Gast verbindet sein Handy mit deinem Heim-WLAN, fügt in seiner Companion-App deine interne Home-Assistant-Adresse hinzu und meldet sich mit dem Gastkonto an. Gib ihm den Companion-Link oder die Schaltfläche im Dashboard.

Beim Teilen über den Browser verwendet der Gast-QR-Code die interne Home-Assistant-Adresse. Fehlt der QR-Code, prüfe die interne URL unter **Einstellungen → System → Netzwerk** und ob das Gastgerät sie erreichen kann.

## Die Browser-Web-App installieren

1. Öffne unter **Teilen** auf Android **Zum Installieren in Chrome öffnen**. Wenn dein Handy die Seite in Home Assistant lässt, tippe auf **Browser-Link kopieren**, öffne Chrome als eigene App und füge den Link in dessen Adressleiste ein. Auf anderen Geräten kannst du **Auf diesem Gerät installieren** verwenden. Für die Browser-Installation braucht das Zielgerät eine erreichbare HTTPS-Adresse mit gültigem Zertifikat.
2. Melde dich bei Home Assistant an, falls der Browser danach fragt. Auf iPhone und iPad öffnest du den Link in Safari und wählst **Teilen → Zum Home-Bildschirm**. Aktiviere **Als Web-App öffnen**, wenn Safari die Option zeigt. Auf Android tippe auf **Jetzt installieren**, wenn Chrome den Dialog anbietet. Sonst öffne das Chrome-Menü **⋮ → Installieren und Verknüpfung erstellen → Installieren**. Die Bezeichnung kann je nach Chrome-Version abweichen. Am Computer verwendest du die Installationsoption deines Browsers, sofern er sie anbietet. [Anleitung von Apple](https://support.apple.com/de-de/guide/iphone/iphea86e5236/ios) · [Anleitung für Chrome](https://support.google.com/chrome/answer/9658361?hl=de)
3. Öffne die App über das Symbol auf dem Startbildschirm. Die eigenständig installierte App verwendet ihre Browsersitzung. Wenn dort noch keine Sitzung vorhanden ist, zeigt Home Assistant die Anmeldung an.

Mit **Link teilen** öffnest du das Teilen-Menü deines Geräts. **Browser-Link kopieren** gibt dir dieselbe URL wie der QR-Code zum Einfügen.

Der Offline-Cache speichert die App-Hülle, das Symbol und weitere öffentliche Dateien. Karten, aktuelle Zustände und die Bedienung deiner Geräte brauchen eine Verbindung zu Home Assistant.

## Fragen oder etwas klappt nicht?

- **Zugriff verweigert.** Prüfe, welches Konto angemeldet ist und ob es unter **Zugriff** freigegeben wurde. Bei Gästen muss das Handy die interne Adresse aus deinem Heimnetz erreichen.
- **Der Companion-Link bleibt als Text stehen.** Verwende eine Schaltfläche im Dashboard mit dem relativen Pfad aus dem Designer.
- **Die Installationsoption fehlt.** Öffne den Browser-Link auf iPhone oder iPad in Safari. Verwende auf anderen Geräten einen Chromium-Browser mit App-Installation und prüfe, ob sich die HTTPS-Adresse ohne Zertifikatfehler öffnen lässt.
- **Eine Karte fehlt.** Prüfe die Karte zuerst in Home Assistant mit demselben Konto. Bei einer benutzerdefinierten Karte prüfe auch, ob ihre Ressource im Frontend verfügbar ist.

Wenn du festhängst, gib am besten deine Core-Version, die Studio-Version, das Gerät und die Schritte an, mit denen sich das Problem nachstellen lässt. [Problem melden](https://github.com/seb5594/hass-pwa_app_studio-integration/issues) · [Versionsverlauf](CHANGELOG.md) · [Architektur](docs/architekturpruefung.md)
