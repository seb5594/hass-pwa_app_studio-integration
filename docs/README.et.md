# Veebirakenduse installimine, sidumine ja värskendamine

## Saatke armatuurlaud kellelegi, keda tunnete

Näide. Sebastian loob veebirakenduse, mis näitab rongide väljumisi. Tema onu kasutab juba ametlikku rakendust Home Assistant Companion ja tal on juurdepääs armatuurlauale. Sebastian saadab brauseri lingi WhatsApp kaudu.

1. PWA Web-App Studio-s avage rakendus, avage Access, lubage kaasrakenduse kaudu sisselogimine ja salvestage. Mõlemad rakendused peavad jõudma HTTPS-i kaudu samasse Home Assistant serverisse.

2. Teie külaline avab oma brauseris lingi WhatsApp ja valib Logi sisse kaasrakenduse kaudu. Veebirakendus kuvab seadme koodi. Külaline saab seda vajadusel kopeerida.

3. Puudutage valikut Ava Home Assistant. Veenduge, et rakendus, konto ja kood ühtivad. Kui sidumisleht küsib koodi, kleepige või sisestage veebirakenduses kuvatav kood. Seejärel kinnitage sisselogimine.

4. Lülitage tagasi algsele brauseri vahekaardile. See logib automaatselt sisse. Vajadusel toksake Kontrolli kinnitust. Kood kehtib viis minutit ja ühe sisselogimise kohta.

5. IPhone'is või iPadis installitud koopiasse sisselogimiseks lisage leht esmalt Safari avakuvale. Avage avakuva ikoon ja alustage seal sama kinnitamisprotsessi.

## Otsige üles stuudio

Kasutage integreerimisseadet, seejärel avage stuudio Home Assistant dialoogi kaudu. Kui töötate rakendustega sageli, lubage integreerimisseadetes külgriba paneeli lüliti olem ja lülitage see sisse, et otsetee oleks nähtav.

Hoolduse armatuurlaua jaoks lisage nupukaart, mis navigeerib numbrile /pwa-app-studio. Valikuline nupp Ava PWA Designer saab selle avada ka teie aktiivses administraatoriseansis. Esmalt lubage see olem; Home Assistant keelab selle vaikimisi.

## Kujundage ja värskendage külaliste armatuurlauda

Näiteks looge Wi-Fi teabekaardi ja terrassivalgustiga külastajatele armatuurlaud. Valige jaotises Sisu üksikud kaardid ja valige eelseadistus või importige olemasolev kaart. Määrake pealkiri, olem või Markdown visuaalse redaktori abil ja kontrollige telefoni eelvaadet.

Rakenduse etapis määrake rakenduse versiooniks 1.1 ja salvestage. Külaline, kellel on rakendus endiselt avatud, näeb värskendusbännerit, kui rakendus tuvastab uue versiooni. Kui puudutate valikut Värskenda rakendust, laaditakse vaade uuesti ja säilib avaekraani ikoon ja brauseri seanss. Hiljem avatud rakendus laadib ühenduse loomisel praeguse versiooni.

## Jaga Androidist

Kasutage lingi jagamist Studios. Omadialoog avaneb, kui rakendus või brauser seda pakub. Kui kaasrakendus ei paku jagamise API-t, avage brauseris jagamisleht. Võite ka lingi kopeerida.

[English README](../README.md) · [Deutsch](../README.de.md)
