# Instalați, asociați și actualizați o aplicație web

## Trimiteți un tablou de bord unei persoane cunoscute

Exemplu. Sebastian creează o aplicație web care arată plecările trenurilor. Unchiul său folosește deja aplicația oficială Home Assistant Companion și are acces la tabloul de bord. Sebastian trimite link-ul browserului prin WhatsApp.

1. În PWA Web-App Studio, deschideți aplicația, accesați Acces, activați conectarea prin aplicația Companion și salvați. Ambele aplicații trebuie să ajungă la același server Home Assistant prin HTTPS.

2. Invitatul dvs. deschide linkul WhatsApp în browser și alege Conectați-vă prin aplicația însoțitoare. Aplicația web afișează un cod de dispozitiv. Oaspetele îl poate copia dacă este necesar.

3. Atinge Deschide Home Assistant. Confirmați că aplicația, contul și codul se potrivesc. Dacă pagina de asociere solicită un cod, inserați sau introduceți codul afișat în aplicația web. Apoi aprobați conectarea.

4. Reveniți la fila originală a browserului. Se conectează automat. Dacă este necesar, atingeți Verificați aprobarea. Codul este valabil timp de cinci minute și pentru o singură conectare.

5. Pe iPhone sau iPad, pentru a vă conecta la copia instalată, adăugați mai întâi pagina la ecranul de pornire din Safari. Deschideți pictograma Ecran de pornire și începeți același proces de aprobare acolo.

## Găsiți Studioul

Utilizați echipamentul de integrare, apoi deschideți Studioul prin dialogul Home Assistant. Dacă lucrați frecvent la aplicații, activați entitatea de comutare a panoului din bara laterală în setările de integrare și activați-o pentru a menține vizibilă comanda rapidă.

Pentru un tablou de bord de întreținere, adăugați un card cu buton care navighează la /pwa-app-studio. Entitatea opțională butonul Open PWA Designer o poate deschide și în sesiunea dvs. activă de administrator. Activați mai întâi acea entitate; Home Assistant îl dezactivează implicit.

## Proiectați și actualizați un tablou de bord pentru invitați

De exemplu, creați un tablou de bord pentru vizitatori cu un card de informații Wi-Fi și o lumină de terasă. Sub Conținut, alegeți carduri individuale și selectați o presetare sau importați un card existent. Setați titlul, entitatea sau Markdown utilizând editorul vizual și verificați previzualizarea telefonului.

În pasul Aplicație, setați versiunea aplicației la 1.1 și salvați. Un oaspete care are încă aplicația deschisă vede un banner de actualizare atunci când aplicația detectează noua revizuire. Atingerea aplicației Actualizare reîncarcă vizualizarea și păstrează pictograma de pe ecranul de pornire și sesiunea browserului. O aplicație deschisă ulterior încarcă versiunea curentă atunci când este conectată.

## Distribuie de pe Android

Utilizați partajarea prin link în Studio. Dialogul nativ se deschide atunci când aplicația sau browserul îl furnizează. Dacă aplicația Companion nu oferă API de partajare, deschideți pagina de partajare în browser. De asemenea, puteți copia linkul.

[English README](../README.md) · [Deutsch](../README.de.md)
