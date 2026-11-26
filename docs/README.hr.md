# Instalirajte, uparite i ažurirajte web aplikaciju

## Pošaljite nadzornu ploču nekome koga poznajete

Primjer. Sebastian stvara web aplikaciju koja prikazuje polaske vlakova. Njegov ujak već koristi službenu aplikaciju Home Assistant Companion i ima pristup nadzornoj ploči. Sebastian šalje vezu preglednika putem WhatsApp.

1. U PWA Web-App Studio otvorite aplikaciju, idite na Access, omogućite prijavu putem Companion aplikacije i spremite. Obje aplikacije moraju doći do istog poslužitelja Home Assistant putem HTTPS-a.

2. Vaš gost otvara poveznicu WhatsApp u svom pregledniku i odabire Prijava putem aplikacije Companion. Web aplikacija prikazuje kod uređaja. Gost ga može kopirati ako je potrebno.

3. Dodirnite Otvori Home Assistant. Potvrdite podudaranje aplikacije, računa i koda. Ako stranica za uparivanje traži kod, zalijepite ili unesite kod prikazan u web-aplikaciji. Zatim odobrite prijavu.

4. Vratite se na izvornu karticu preglednika. Prijavljuje se automatski. Ako je potrebno, dodirnite Provjeri odobrenje. Kod vrijedi pet minuta i za jednu prijavu.

5. Na iPhoneu ili iPadu, da biste se prijavili na instaliranu kopiju, prvo dodajte stranicu na početni zaslon u Safariju. Otvorite ikonu početnog zaslona i tamo pokrenite isti postupak odobravanja.

## Pronađite studio

Upotrijebite opremu za integraciju, zatim otvorite Studio kroz dijaloški okvir Home Assistant. Ako često radite na aplikacijama, omogućite entitet prekidača bočne trake u postavkama integracije i uključite ga kako bi prečac ostao vidljiv.

Za nadzornu ploču za održavanje, dodajte karticu gumba koja vodi do /pwa-app-studio. Opcijski entitet gumba Open PWA Designer također ga može otvoriti u vašoj aktivnoj administratorskoj sesiji. Prvo omogućite taj entitet; Home Assistant ga onemogućuje prema zadanim postavkama.

## Dizajnirajte i ažurirajte nadzornu ploču za goste

Na primjer, izradite nadzornu ploču za posjetitelje s Wi-Fi informacijskom karticom i rasvjetom na terasi. U odjeljku Sadržaj odaberite pojedinačne kartice i odaberite unaprijed postavljenu karticu ili uvezite postojeću karticu. Postavite naslov, entitet ili Markdown pomoću vizualnog uređivača i provjerite telefonski pregled.

U koraku aplikacije postavite verziju aplikacije na 1.1 i spremite. Gost koji još uvijek ima otvorenu aplikaciju vidi natpis ažuriranja kada aplikacija otkrije novu reviziju. Dodirom Ažuriraj aplikaciju ponovno se učitava prikaz i zadržava ikona početnog zaslona i sesija preglednika. Aplikacija otvorena kasnije učitava trenutnu verziju kada se poveže.

## Podijelite s Androida

Koristite dijeljenje veze u Studiju. Izvorni dijaloški okvir otvara se kada ga aplikacija ili preglednik omogući. Ako aplikacija Companion ne nudi API za dijeljenje, otvorite stranicu za dijeljenje u pregledniku. Također možete kopirati vezu.

[English README](../README.md) · [Deutsch](../README.de.md)
