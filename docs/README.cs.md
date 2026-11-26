# Nainstalujte, spárujte a aktualizujte webovou aplikaci

## Pošlete řídicí panel někomu, koho znáte

Example. Sebastian creates a web app that shows train departures. His uncle already uses the official Home Assistant Companion App and has access to the dashboard. Sebastian sends the browser link via WhatsApp.

1. V PWA Web-App Studio otevřete aplikaci, přejděte do Accessu, povolte přihlášení přes Companion App a uložte. Obě aplikace musí přes HTTPS dosáhnout stejného serveru Home Assistant.

2. Váš host otevře odkaz WhatsApp ve svém prohlížeči a zvolí Přihlásit se prostřednictvím aplikace Companion. Webová aplikace zobrazí kód zařízení. V případě potřeby si jej host může zkopírovat.

3. Tap Open Home Assistant. Potvrďte, že se aplikace, účet a kód shodují. Pokud stránka pro párování požaduje kód, vložte nebo zadejte kód zobrazený ve webové aplikaci. Poté schválte přihlášení.

4. Switch back to the original browser tab. Přihlašuje se automaticky. V případě potřeby klepněte na Zkontrolovat schválení. Kód je platný po dobu pěti minut a na jedno přihlášení.

5. Chcete-li se na iPhonu nebo iPadu přihlásit k nainstalované kopii, nejprve přidejte stránku na domovskou obrazovku v Safari. Otevřete ikonu domovské obrazovky a spusťte stejný schvalovací proces tam.

## Najděte Studio

Použijte integrační zařízení a poté otevřete Studio prostřednictvím dialogu Home Assistant. Pokud s aplikacemi pracujete často, povolte v nastavení integrace entitu přepínače panelu postranního panelu a zapněte ji, aby byla zkratka viditelná.

Pro řídicí panel údržby přidejte kartu tlačítka, která naviguje na /pwa-app-studio. Volitelná entita tlačítka Open PWA Designer jej také může otevřít ve vaší aktivní administrátorské relaci. Nejprve povolte tuto entitu; Home Assistant disables it by default.

## Design and update a guest dashboard

Například vytvořte palubní desku pro návštěvníky s informační kartou Wi-Fi a osvětlením terasy. V části Obsah vyberte jednotlivé karty a vyberte předvolbu nebo importujte existující kartu. Pomocí vizuálního editoru nastavte název, entitu nebo Markdown a zkontrolujte náhled telefonu.

V kroku Aplikace nastavte verzi aplikace na 1.1 a uložte. Host, který má aplikaci stále otevřenou, uvidí aktualizační banner, když aplikace zjistí novou revizi. Klepnutím na Aktualizovat aplikaci znovu načte zobrazení a zachová ikonu domovské obrazovky a relaci prohlížeče. Aplikace, která se otevře později, po připojení načte aktuální verzi.

## Sdílet ze systému Android

Použijte sdílení odkazů ve Studiu. Nativní dialog se otevře, když jej aplikace nebo prohlížeč poskytne. Pokud Companion App nenabízí žádné sdílené API, otevřete stránku sdílení v prohlížeči. Můžete také zkopírovat odkaz.

[English README](../README.md) · [Deutsch](../README.de.md)
