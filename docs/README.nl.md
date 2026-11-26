# Installeer, koppel en update een webapp

## Stuur een dashboard naar iemand die je kent

Voorbeeld. Sebastian maakt een webapp die het vertrek van treinen laat zien. Zijn oom gebruikt al de officiële Home Assistant Companion App en heeft toegang tot het dashboard. Sebastian stuurt de browserlink via WhatsApp.

1. Open in PWA Web-App Studio de app, ga naar Toegang, schakel inloggen via de Companion App in en sla op. Beide apps moeten via HTTPS dezelfde Home Assistant-server bereiken.

2. Uw gast opent de link WhatsApp in zijn browser en kiest Aanmelden via de Companion App. De webapp geeft een apparaatcode weer. De gast kan het indien nodig kopiëren.

3. Tik op Home Assistant openen. Bevestig dat de app, het account en de code overeenkomen. Als de koppelingspagina om een ​​code vraagt, plakt of typt u de code die in de webapp wordt weergegeven. Keur vervolgens het inloggen goed.

4. Schakel terug naar het oorspronkelijke browsertabblad. Het logt automatisch in. Tik indien nodig op Goedkeuring controleren. De code is vijf minuten geldig en voor één keer inloggen.

5. Om op iPhone of iPad in te loggen op het geïnstalleerde exemplaar, voegt u eerst de pagina toe aan het startscherm in Safari. Open het startschermpictogram en start daar hetzelfde goedkeuringsproces.

## Zoek de studio

Gebruik de integratieapparatuur en open vervolgens de Studio via het dialoogvenster Home Assistant. Als u vaak aan apps werkt, schakelt u de schakelentiteit Zijbalkpaneel in de integratie-instellingen in en schakelt u deze in om de snelkoppeling zichtbaar te houden.

Voeg voor een onderhoudsdashboard een knoppenkaart toe die naar /pwa-app-studio navigeert. De optionele knopentiteit Open PWA Designer kan deze ook openen in uw actieve beheerderssessie. Schakel eerst die entiteit in; Home Assistant schakelt dit standaard uit.

## Ontwerp en update een gastendashboard

Maak bijvoorbeeld een dashboard voor bezoekers met een Wi-Fi-informatiekaart en terrasverlichting. Kies onder Inhoud individuele kaarten en selecteer een voorinstelling of importeer een bestaande kaart. Stel de titel, entiteit of Markdown in met behulp van de visuele editor en bekijk het telefoonvoorbeeld.

Stel in de App-stap de App-versie in op 1.1 en sla deze op. Een gast die de app nog open heeft, ziet een updatebanner wanneer de app de nieuwe revisie detecteert. Als u op Update app tikt, wordt de weergave opnieuw geladen en blijven het startschermpictogram en de browsersessie behouden. Een app die later wordt geopend, laadt de huidige versie wanneer deze is verbonden.

## Deel vanaf Android

Gebruik het delen van links in de Studio. Het oorspronkelijke dialoogvenster wordt geopend wanneer de app of browser dit biedt. Als de Companion App geen deel-API biedt, open dan de deelpagina in de browser. Je kunt de link ook kopiëren.

[English README](../README.md) · [Deutsch](../README.de.md)
