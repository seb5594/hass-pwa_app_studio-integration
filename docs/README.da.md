# Installer, par og opdater en webapp

## Send et betjeningspanel til en, du kender

Eksempel. Sebastian laver en webapp, der viser togafgange. Hans onkel bruger allerede den officielle Home Assistant Companion App og har adgang til dashboardet. Sebastian sender browserlinket via WhatsApp.

1. I PWA Web-App Studio skal du åbne appen, gå til Access, aktivere login via Companion-appen og gemme. Begge apps skal nå den samme Home Assistant-server over HTTPS.

2. Din gæst åbner linket WhatsApp i deres browser og vælger Log ind via Companion-appen. Webappen viser en enhedskode. Gæsten kan kopiere den, hvis det er nødvendigt.

3. Tryk på Åbn Home Assistant. Bekræft, at appen, kontoen og koden matcher. Hvis parringssiden beder om en kode, skal du indsætte eller indtaste koden vist i webappen. Godkend derefter login.

4. Skift tilbage til den oprindelige browserfane. Den logger automatisk ind. Tryk om nødvendigt på Tjek godkendelse. Koden er gyldig i fem minutter og til ét login.

5. På iPhone eller iPad skal du først tilføje siden til startskærmen i Safari for at logge ind på den installerede kopi. Åbn startskærmikonet og start den samme godkendelsesproces der.

## Find studiet

Brug integrationsudstyret, og åbn derefter studiet gennem Home Assistant-dialogen. Hvis du ofte arbejder på apps, skal du aktivere skiftenheden i sidepanelpanelet i integrationsindstillingerne og slå den til for at holde genvejen synlig.

Til et vedligeholdelsesdashboard skal du tilføje et knapkort, der navigerer til /pwa-app-studio. Den valgfri Open PWA Designer-knap-entitet kan også åbne den i din aktive administratorsession. Aktiver først den enhed; Home Assistant deaktiverer det som standard.

## Design og opdater et gæstedashboard

Lav for eksempel et dashboard til besøgende med et Wi-Fi-informationskort og en terrasselampe. Under Indhold skal du vælge individuelle kort og vælge en forudindstilling eller importere et eksisterende kort. Indstil titlen, entiteten eller Markdown ved hjælp af den visuelle editor, og tjek telefonens forhåndsvisning.

Indstil App-version til 1.1 i app-trinnet og gem. En gæst, der stadig har appen åben, ser et opdateringsbanner, når appen registrerer den nye revision. Hvis du trykker på Opdater app, genindlæses visningen og beholder startskærmsikonet og browsersessionen. En app, der åbnes senere, indlæser den aktuelle version, når den er tilsluttet.

## Del fra Android

Brug linkdeling i studiet. Den indbyggede dialog åbnes, når appen eller browseren leverer den. Hvis Companion-appen ikke tilbyder nogen share API, skal du åbne delesiden i browseren. Du kan også kopiere linket.

[English README](../README.md) · [Deutsch](../README.de.md)
