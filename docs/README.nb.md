# Installer, par og oppdater en nettapp

## Send et dashbord til noen du kjenner

Eksempel. Sebastian lager en nettapp som viser togavganger. Onkelen hans bruker allerede den offisielle Home Assistant Companion-appen og har tilgang til dashbordet. Sebastian sender nettleserlenken via WhatsApp.

1. I PWA Web-App Studio åpner du appen, går til Access, aktiverer pålogging via Companion-appen og lagrer. Begge appene må nå den samme Home Assistant-serveren over HTTPS.

2. Gjesten din åpner WhatsApp-lenken i nettleseren sin og velger Logg på via Companion-appen. Nettappen viser en enhetskode. Gjesten kan kopiere den ved behov.

3. Trykk på Åpne Home Assistant. Bekreft at appen, kontoen og koden samsvarer. Hvis sammenkoblingssiden ber om en kode, lim inn eller skriv inn koden som vises i nettappen. Godkjenn deretter pålogging.

4. Bytt tilbake til den opprinnelige nettleserfanen. Den logger på automatisk. Trykk om nødvendig på Sjekk godkjenning. Koden er gyldig i fem minutter og for én pålogging.

5. På iPhone eller iPad, for å logge på den installerte kopien, må du først legge til siden på startskjermen i Safari. Åpne startskjermikonet og start den samme godkjenningsprosessen der.

## Finn studioet

Bruk integreringsutstyret, og åpne deretter Studioet gjennom Home Assistant-dialogen. Hvis du jobber med apper ofte, aktiverer du sidepanel-bryterenheten i integreringsinnstillingene og slår den på for å holde snarveien synlig.

For et vedlikeholdsdashbord, legg til et knappekort som navigerer til /pwa-app-studio. Den valgfrie Open PWA Designer-knappenheten kan også åpne den i den aktive administratorøkten. Aktiver den enheten først; Home Assistant deaktiverer den som standard.

## Design og oppdater et gjestedashbord

Lag for eksempel et dashbord for besøkende med et Wi-Fi-informasjonskort og en terrasselys. Under Innhold velger du individuelle kort og velger en forhåndsinnstilling eller importerer et eksisterende kort. Angi tittelen, enheten eller Markdown ved hjelp av det visuelle redigeringsprogrammet og sjekk telefonens forhåndsvisning.

I app-trinnet setter du appversjon til 1.1 og lagrer. En gjest som fortsatt har appen åpen, ser et oppdateringsbanner når appen oppdager den nye revisjonen. Å trykke på Oppdater-appen laster visningen på nytt og beholder startskjermikonet og nettleserøkten. En app som åpnes senere laster den gjeldende versjonen når den er tilkoblet.

## Del fra Android

Bruk koblingsdeling i studioet. Den opprinnelige dialogboksen åpnes når appen eller nettleseren gir den. Hvis Companion-appen ikke tilbyr noen delings-API, åpner du delingssiden i nettleseren. Du kan også kopiere lenken.

[English README](../README.md) · [Deutsch](../README.de.md)
