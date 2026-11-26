# Asenna, yhdistä ja päivitä verkkosovellus

## Lähetä kojelauta jollekin tutullesi

Esimerkki. Sebastian luo verkkosovelluksen, joka näyttää junien lähdöt. Hänen setänsä käyttää jo virallista Home Assistant Companion -sovellusta ja hänellä on pääsy kojelautaan. Sebastian lähettää selainlinkin WhatsApp:n kautta.

1. Avaa PWA Web-App Studio:ssä sovellus, siirry Accessiin, ota sisäänkirjautuminen käyttöön Companion Appin kautta ja tallenna. Molempien sovellusten on saavutettava sama Home Assistant-palvelin HTTPS:n kautta.

2. Vieraasi avaa WhatsApp-linkin selaimessaan ja valitsee Kirjaudu sisään kumppanisovelluksen kautta. Verkkosovellus näyttää laitekoodin. Vieras voi tarvittaessa kopioida sen.

3. Napauta Avaa Home Assistant. Varmista, että sovellus, tili ja koodi täsmäävät. Jos pariliitossivu pyytää koodia, liitä tai kirjoita verkkosovelluksessa näkyvä koodi. Hyväksy sitten kirjautuminen.

4. Vaihda takaisin alkuperäiseen selaimen välilehteen. Se kirjautuu sisään automaattisesti. Napauta tarvittaessa Tarkista hyväksyntä. Koodi on voimassa viisi minuuttia ja yhden sisäänkirjautumisen.

5. Jos haluat kirjautua sisään asennettuun kopioon iPhonessa tai iPadissa, lisää sivu ensin Safarin aloitusnäyttöön. Avaa aloitusnäytön kuvake ja aloita sama hyväksyntäprosessi siellä.

## Etsi studio

Käytä integrointivaihdetta ja avaa sitten Studio Home Assistant-valintaikkunan kautta. Jos työskentelet sovellusten parissa usein, ota sivupalkkipaneelin kytkinyksikkö käyttöön integrointiasetuksissa ja ota se käyttöön, jotta pikakuvake pysyy näkyvissä.

Lisää huoltokojelautaan painikekortti, joka navigoi kohtaan /pwa-app-studio. Valinnainen Open PWA Designer -painikekokonaisuus voi myös avata sen aktiivisessa järjestelmänvalvojan istunnossa. Ota tämä entiteetti ensin käyttöön; Home Assistant poistaa sen oletusarvoisesti käytöstä.

## Suunnittele ja päivitä vierashallintapaneeli

Luo esimerkiksi vierailijoille kojelauta, jossa on Wi-Fi-tietokortti ja patiovalo. Valitse Sisältö-kohdasta yksittäiset kortit ja valitse esiasetus tai tuo olemassa oleva kortti. Aseta otsikko, entiteetti tai Markdown visuaalisen editorin avulla ja tarkista puhelimen esikatselu.

Aseta App-vaiheessa sovelluksen versioksi 1.1 ja tallenna. Vieras, jolla on edelleen sovellus auki, näkee päivitysbannerin, kun sovellus havaitsee uuden version. Napauttamalla Päivitä sovellus lataa näkymän uudelleen ja säilyttää aloitusnäytön kuvakkeen ja selainistunnon. Myöhemmin avattu sovellus lataa nykyisen version, kun yhteys on muodostettu.

## Jaa Androidista

Käytä linkin jakamista Studiossa. Alkuperäinen valintaikkuna avautuu, kun sovellus tai selain tarjoaa sen. Jos Companion App ei tarjoa jakosovellusliittymää, avaa jakosivu selaimessa. Voit myös kopioida linkin.

[English README](../README.md) · [Deutsch](../README.de.md)
