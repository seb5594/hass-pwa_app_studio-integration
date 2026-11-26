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

### Das Studio öffnen

Öffne **Einstellungen → Geräte & Dienste → PWA Web-App Studio → Konfigurieren** und folge dem Link zum Designer. Der direkte Pfad lautet `/pwa-app-studio`.

Wenn du regelmäßig an deinen Apps arbeitest, aktiviere in der Entitätenliste der Integration **Sidebar Panel** und schalte es ein. Auf einem Wartungs-Dashboard kannst du stattdessen eine Lovelace-Schaltfläche mit der Aktion **Navigieren** und dem Pfad `/pwa-app-studio` hinterlegen. Die optionale Button-Entität **PWA Designer öffnen** öffnet den Designer in deiner aktiven Admin-Sitzung. Schalter und Button sind bei einer neuen Einrichtung in der Entitätenregistrierung standardmäßig deaktiviert.

1. Wähle unter **Teilen** die Schaltfläche **Zum Installieren im Browser öffnen** oder **Auf diesem Gerät installieren**. Wenn die Seite in Home Assistant bleibt, nutze **Browser-Link kopieren** und füge den Link in deinem Browser ein. Die Web-App braucht HTTPS mit gültigem Zertifikat.
2. Auf iPhone und iPad öffnest du den Link in Safari und wählst **Teilen → Zum Home-Bildschirm**. Aktiviere **Als Web-App öffnen**, falls es angezeigt wird. Auf Android tippe auf **Jetzt installieren**, wenn dein Browser den Dialog anbietet, oder suche im Browsermenü nach **App installieren** oder **Zum Startbildschirm hinzufügen**. [Anleitung von Apple](https://support.apple.com/de-de/guide/iphone/iphea86e5236/ios)
3. Öffne die App über das Symbol auf dem Startbildschirm. Melde dich an, falls du dazu aufgefordert wirst, oder nutze die Freigabe über die Companion-App.

### Die Web-App über die Companion-App freigeben

Beispiel aus der Praxis. Sebastian baut eine Abfahrtsanzeige als Web-App und schickt seinem Onkel den Browser-Link über WhatsApp. Sein Onkel ist schon in der offiziellen Home-Assistant-App angemeldet und hat Zugriff auf die Web-App.

1. Öffne im Studio die gespeicherte App, aktiviere **Zugriff → Anmeldung über die Companion-App erlauben** und speichere. Verwende HTTPS für die Web-App und in der Companion-App. Wähle in beiden denselben Home-Assistant-Server.
2. Öffne den WhatsApp-Link im Browser und wähle **Über die Companion-App anmelden**. Die Seite zeigt den Gerätecode und die Schaltfläche **Code kopieren**. Auf dem iPhone oder iPad öffnest du eine bereits installierte Kopie über ihr Symbol auf dem Home-Bildschirm.
3. Tippe auf **Home Assistant öffnen**. Prüfe Instanz, App und Konto und vergleiche den Code. Falls ein Eingabefeld erscheint, gib den Code ein oder füge ihn ein. Tippe auf **Anmeldung freigeben**. Die Freigabeseite ist auch über eine Dashboard-Schaltfläche mit dem Pfad `/pwa-app-studio-connect` erreichbar.
4. Wechsle zum selben Browser-Tab oder zur installierten Web-App zurück. Die Anmeldung erfolgt automatisch. Du kannst auch auf **Freigabe prüfen** tippen. Jeder Code gilt fünf Minuten und für eine Anmeldung. **Im Browser anmelden** bleibt verfügbar.

Die Web-App bekommt eine eigene Home-Assistant-Sitzung mit den Rechten deines Kontos. Du kannst sie im Home-Assistant-Profil unter **Sicherheit → Aktualisierungstoken** widerrufen.

**Link teilen** nutzt das Teilen-Menü des Geräts, wenn es verfügbar ist. In der Android-Companion-App kann sich die Freigabeseite im Standardbrowser öffnen. Je nach Browser kannst du dort das Browsermenü oder **Browser-Link kopieren** nutzen.

### Ein Gäste-Dashboard gestalten und aktualisieren

Für deine Terrasse kannst du unter **Inhalt → Einzelne Karten auswählen** eine Markdown-Karte mit Infos für Besucher und eine Schaltfläche für das Terrassenlicht anlegen. Bearbeite Titel, Text und Entität direkt in den Kartenfeldern. Prüfe das Ergebnis in der Smartphone-Vorschau und speichere. Weitere Einstellungen findest du unter **Kartenkonfiguration**.

Trage unter **App → App-Version** zum Beispiel `1.1` ein und speichere. Die Version erscheint unten in der Web-App. Hat ein Gast die App offen, erscheint nach der Update-Prüfung **App aktualisieren**. Ein Tipp lädt die Ansicht neu. Das Startbildschirm-Symbol und die Anmeldung bleiben erhalten. Wer die App später online öffnet, bekommt direkt den aktuellen Stand.

Der Offline-Cache speichert die App-Hülle, das Symbol und weitere öffentliche Dateien. Karten, aktuelle Zustände und die Bedienung deiner Geräte brauchen eine Verbindung zu Home Assistant.

## Fragen oder etwas klappt nicht?

- **Zugriff verweigert.** Prüfe, welches Konto angemeldet ist und ob es unter **Zugriff** freigegeben wurde. Bei Gästen muss das Handy die interne Adresse aus deinem Heimnetz erreichen.
- **Der Companion-Link bleibt als Text stehen.** Verwende eine Schaltfläche im Dashboard mit dem relativen Pfad aus dem Designer.
- **Die Installationsoption fehlt.** Prüfe, ob dein Browser die Installation auf dem Startbildschirm unterstützt und ob sich die HTTPS-Adresse ohne Zertifikatfehler öffnen lässt.
- **Eine Karte fehlt.** Prüfe die Karte zuerst in Home Assistant mit demselben Konto. Bei einer benutzerdefinierten Karte prüfe auch, ob ihre Ressource im Frontend verfügbar ist.

Wenn du festhängst, gib am besten deine Core-Version, die Studio-Version, das Gerät und die Schritte an, mit denen sich das Problem nachstellen lässt. [Problem melden](https://github.com/seb5594/hass-pwa_app_studio-integration/issues) · [Versionsverlauf](CHANGELOG.md) · [Architektur](docs/architekturpruefung.md)

## Weitere Sprachen

[Français](docs/README.fr.md) · [Español](docs/README.es.md) · [Italiano](docs/README.it.md) · [Português](docs/README.pt.md) · [Português (Brasil)](docs/README.pt-BR.md) · [Nederlands](docs/README.nl.md) · [Polski](docs/README.pl.md) · [Čeština](docs/README.cs.md) · [Slovenčina](docs/README.sk.md) · [Magyar](docs/README.hu.md) · [Română](docs/README.ro.md) · [Български](docs/README.bg.md) · [Ελληνικά](docs/README.el.md) · [Svenska](docs/README.sv.md) · [Dansk](docs/README.da.md) · [Norsk](docs/README.nb.md) · [Suomi](docs/README.fi.md) · [Українська](docs/README.uk.md) · [Русский](docs/README.ru.md) · [Türkçe](docs/README.tr.md) · [简体中文](docs/README.zh-Hans.md) · [繁體中文](docs/README.zh-Hant.md) · [日本語](docs/README.ja.md) · [العربية](docs/README.ar.md) · [हिन्दी](docs/README.hi.md) · [עברית](docs/README.he.md) · [Bahasa Indonesia](docs/README.id.md) · [Hrvatski](docs/README.hr.md) · [Slovenščina](docs/README.sl.md) · [Eesti](docs/README.et.md) · [Latviešu](docs/README.lv.md) · [Lietuvių](docs/README.lt.md) · [Gaeilge](docs/README.ga.md) · [Malti](docs/README.mt.md) · [Íslenska](docs/README.is.md)

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
