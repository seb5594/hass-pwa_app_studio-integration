# Nainštalujte, spárujte a aktualizujte webovú aplikáciu

## Pošlite informačný panel niekomu, koho poznáte

Example. Sebastian creates a web app that shows train departures. His uncle already uses the official Home Assistant Companion App and has access to the dashboard. Sebastian sends the browser link via WhatsApp.

1. V PWA Web-App Studio otvorte aplikáciu, prejdite na Access, povoľte prihlásenie cez Companion App a uložte. Obe aplikácie musia dosiahnuť rovnaký server Home Assistant cez HTTPS.

2. Váš hosť otvorí odkaz WhatsApp vo svojom prehliadači a vyberie Prihlásiť sa cez aplikáciu Companion. Webová aplikácia zobrazí kód zariadenia. V prípade potreby si ho môže hosť skopírovať.

3. Klepnite na Otvoriť Home Assistant. Potvrďte, že sa aplikácia, účet a kód zhodujú. Ak si párovacia stránka vyžiada kód, prilepte alebo zadajte kód zobrazený vo webovej aplikácii. Potom schváľte prihlásenie.

4. Prepnúť späť na pôvodnú kartu prehliadača. Prihlasuje sa automaticky. V prípade potreby klepnite na Skontrolovať schválenie. Kód je platný päť minút a na jedno prihlásenie.

5. Na zariadení iPhone alebo iPad sa do nainštalovanej kópie prihlásite tak, že najprv pridáte stránku na domovskú obrazovku v prehliadači Safari. Otvorte ikonu Domovskej obrazovky a spustite rovnaký proces schvaľovania.

## Nájdite štúdio

Použite integračné zariadenie a potom otvorte Štúdio cez dialógové okno Home Assistant. Ak často pracujete s aplikáciami, povoľte entitu prepínača bočného panela v nastaveniach integrácie a zapnite ju, aby bola skratka viditeľná.

Pre palubnú dosku údržby pridajte kartu tlačidla, ktorá naviguje na /pwa-app-studio. Voliteľná entita tlačidla Open PWA Designer ho môže otvoriť aj vo vašej aktívnej relácii správcu. Najprv povoľte túto entitu; Home Assistant ho predvolene zakáže.

## Navrhnite a aktualizujte informačný panel hosťa

Napríklad vytvorte palubnú dosku pre návštevníkov s informačnou kartou Wi-Fi a terasovým svetlom. V časti Obsah vyberte jednotlivé karty a vyberte predvoľbu alebo importujte existujúcu kartu. Nastavte názov, entitu alebo Markdown pomocou vizuálneho editora a skontrolujte náhľad telefónu.

V kroku App nastavte verziu aplikácie na 1.1 a uložte. Hosťovi, ktorý má aplikáciu stále otvorenú, sa zobrazí aktualizačný banner, keď aplikácia zistí novú revíziu. Klepnutím na Aktualizovať aplikáciu znova načítate zobrazenie a zachováte ikonu na domovskej obrazovke a reláciu prehliadača. Aplikácia otvorená neskôr načíta po pripojení aktuálnu verziu.

## Zdieľať zo systému Android

Použite zdieľanie odkazom v Štúdiu. Natívne dialógové okno sa otvorí, keď ho aplikácia alebo prehliadač poskytne. Ak Companion App neponúka žiadne zdieľané API, otvorte stránku zdieľania v prehliadači. Môžete tiež skopírovať odkaz.

[English README](../README.md) · [Deutsch](../README.de.md)
