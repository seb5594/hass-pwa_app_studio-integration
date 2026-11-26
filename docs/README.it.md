# Installa, associa e aggiorna un'app Web

## Invia una dashboard a qualcuno che conosci

Esempio. Sebastian crea un'app Web che mostra le partenze dei treni. Suo zio utilizza già la Companion App ufficiale Home Assistant e ha accesso al dashboard. Sebastian invia il collegamento del browser tramite WhatsApp.

1. In PWA Web-App Studio, apri l'app, vai su Accesso, abilita l'accesso tramite l'app complementare e salva. Entrambe le app devono raggiungere lo stesso server Home Assistant tramite HTTPS.

2. Il tuo ospite apre il collegamento WhatsApp nel proprio browser e sceglie Accedi tramite l'app complementare. L'app Web visualizza un codice dispositivo. L'ospite può copiarlo se necessario.

3. Tocca Apri Home Assistant. Verifica che l'app, l'account e il codice corrispondano. Se la pagina di abbinamento richiede un codice, incolla o inserisci il codice mostrato nell'app web. Quindi approva l'accesso.

4. Torna alla scheda del browser originale. Si accede automaticamente. Se necessario, tocca Verifica approvazione. Il codice è valido per cinque minuti e per un accesso.

5. Su iPhone o iPad, per accedere alla copia installata, aggiungere prima la pagina alla schermata principale di Safari. Apri l'icona della schermata iniziale e avvia lì lo stesso processo di approvazione.

## Trova lo Studio

Utilizzare l'attrezzatura di integrazione, quindi aprire Studio tramite la finestra di dialogo Home Assistant. Se lavori spesso sulle app, abilita l'entità Cambia pannello della barra laterale nelle impostazioni di integrazione e attivala per mantenere visibile il collegamento.

Per un dashboard di manutenzione, aggiungere una scheda pulsante che porta a /pwa-app-studio. L'entità pulsante facoltativo Apri PWA Designer può anche aprirlo nella sessione di amministratore attiva. Abilita prima quell'entità; Home Assistant lo disabilita per impostazione predefinita.

## Progetta e aggiorna una dashboard ospite

Ad esempio, crea una dashboard per i visitatori con una scheda informativa Wi-Fi e una luce nel patio. In Contenuto, scegli le singole carte e seleziona una preimpostazione o importa una carta esistente. Imposta il titolo, l'entità o Markdown utilizzando l'editor visivo e controlla l'anteprima del telefono.

Nel passaggio App impostare la versione dell'app su 1.1 e salvare. Un ospite che ha ancora l'app aperta vede un banner di aggiornamento quando l'app rileva la nuova revisione. Toccando Aggiorna app si ricarica la visualizzazione e si mantengono l'icona della schermata iniziale e la sessione del browser. Un'app aperta successivamente carica la versione corrente quando è connessa.

## Condividi da Android

Utilizza la condivisione dei collegamenti in Studio. La finestra di dialogo nativa si apre quando l'app o il browser la forniscono. Se l'app complementare non offre API di condivisione, apri la pagina di condivisione nel browser. Puoi anche copiare il collegamento.

[English README](../README.md) · [Deutsch](../README.de.md)
