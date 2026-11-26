# Namestite, seznanite in posodobite spletno aplikacijo

## Pošlji nadzorno ploščo nekomu, ki ga poznaš

Primer. Sebastian ustvari spletno aplikacijo, ki prikazuje odhode vlakov. Njegov stric že uporablja uradno aplikacijo Home Assistant Companion in ima dostop do armaturne plošče. Sebastian pošlje povezavo do brskalnika prek WhatsApp.

1. V PWA Web-App Studio odprite aplikacijo, pojdite na Access, omogočite prijavo prek spremljevalne aplikacije in shranite. Obe aplikaciji morata doseči isti strežnik Home Assistant prek HTTPS.

2. Vaš gost odpre povezavo WhatsApp v svojem brskalniku in izbere Prijava prek spremljevalne aplikacije. Spletna aplikacija prikaže kodo naprave. Gost ga lahko po potrebi kopira.

3. Tapnite Odpri Home Assistant. Potrdite, da se aplikacija, račun in koda ujemajo. Če stran za seznanjanje zahteva kodo, prilepite ali vnesite kodo, prikazano v spletni aplikaciji. Nato odobrite prijavo.

4. Preklopite nazaj na prvotni zavihek brskalnika. Samodejno se prijavi. Po potrebi tapnite Preveri odobritev. Koda velja pet minut in za eno prijavo.

5. V iPhonu ali iPadu se za vpis v nameščeno kopijo najprej dodajte stran na začetni zaslon v brskalniku Safari. Odprite ikono začetnega zaslona in tam začnite isti postopek odobritve.

## Poiščite studio

Uporabite orodje za integracijo, nato odprite Studio prek pogovornega okna Home Assistant. Če pogosto delate z aplikacijami, omogočite stikalno entiteto stranske plošče v nastavitvah integracije in jo vklopite, da bo bližnjica vidna.

Za nadzorno ploščo za vzdrževanje dodajte kartico z gumbom, ki vodi do /pwa-app-studio. Izbirna entiteta gumba Open PWA Designer ga lahko odpre tudi v vaši aktivni skrbniški seji. Najprej omogočite to entiteto; Home Assistant ga privzeto onemogoči.

## Oblikujte in posodobite nadzorno ploščo za goste

Ustvarite na primer nadzorno ploščo za obiskovalce z informacijsko kartico Wi-Fi in terasno lučjo. V razdelku Vsebina izberite posamezne kartice in izberite prednastavitev ali uvozite obstoječo kartico. Z vizualnim urejevalnikom nastavite naslov, entiteto ali Markdown in preverite predogled telefona.

V koraku aplikacije nastavite različico aplikacije na 1.1 in shranite. Gost, ki ima aplikacijo še odprto, vidi pasico za posodobitev, ko aplikacija zazna novo različico. Če tapnete Posodobi aplikacijo, znova naložite pogled in ohranite ikono začetnega zaslona ter sejo brskalnika. Pozneje odprta aplikacija naloži trenutno različico, ko je povezana.

## Delite iz Androida

Uporabite skupno rabo povezave v Studiu. Izvorno pogovorno okno se odpre, ko ga zagotovi aplikacija ali brskalnik. Če aplikacija Companion ne ponuja API-ja za skupno rabo, odprite stran za skupno rabo v brskalniku. Povezavo lahko tudi kopirate.

[English README](../README.md) · [Deutsch](../README.de.md)
