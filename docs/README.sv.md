# Installera, koppla ihop och uppdatera en webbapp

## Skicka en instrumentpanel till någon du känner

Exempel. Sebastian skapar en webbapp som visar tågavgångar. Hans farbror använder redan den officiella Home Assistant Companion-appen och har tillgång till instrumentpanelen. Sebastian skickar webbläsarlänken via WhatsApp.

1. I PWA Web-App Studio, öppna appen, gå till Access, aktivera inloggning via Companion-appen och spara. Båda apparna måste nå samma Home Assistant-server via HTTPS.

2. Din gäst öppnar länken WhatsApp i sin webbläsare och väljer Logga in via Companion-appen. Webbappen visar en enhetskod. Gästen kan kopiera den vid behov.

3. Tryck på Öppna Home Assistant. Bekräfta att appen, kontot och koden matchar. Om kopplingssidan ber om en kod, klistra in eller ange koden som visas i webbappen. Godkänn sedan inloggning.

4. Växla tillbaka till den ursprungliga webbläsarfliken. Den loggar in automatiskt. Om det behövs, tryck på Kontrollera godkännande. Koden är giltig i fem minuter och för en inloggning.

5. På iPhone eller iPad, för att logga in på den installerade kopian, lägg först till sidan på startskärmen i Safari. Öppna hemskärmsikonen och starta samma godkännandeprocess där.

## Hitta studion

Använd integreringsväxeln och öppna sedan Studion genom Home Assistant-dialogen. Om du ofta arbetar med appar, aktivera sidofältspanelens växlingsenhet i integrationsinställningarna och aktivera den för att hålla genvägen synlig.

För en underhållsinstrumentpanel, lägg till ett knappkort som navigerar till /pwa-app-studio. Den valfria knappen Öppna PWA Designer kan också öppna den i din aktiva administratörssession. Aktivera den enheten först; Home Assistant inaktiverar det som standard.

## Designa och uppdatera en gästpanel

Skapa till exempel en instrumentpanel för besökare med ett Wi-Fi-informationskort och en uteplatsbelysning. Under Innehåll väljer du enskilda kort och väljer en förinställning eller importerar ett befintligt kort. Ställ in titeln, enheten eller Markdown med hjälp av den visuella redigeraren och kontrollera telefonens förhandsvisning.

I appsteget ställ in appversionen till 1.1 och spara. En gäst som fortfarande har appen öppen ser en uppdateringsbanner när appen upptäcker den nya versionen. Om du trycker på Uppdatera app laddas om vyn och behåller hemskärmsikonen och webbläsarsessionen. En app som öppnas senare laddar den aktuella versionen när den är ansluten.

## Dela från Android

Använd länkdelning i studion. Den inbyggda dialogrutan öppnas när appen eller webbläsaren tillhandahåller den. Om Companion-appen inte erbjuder något delings-API öppnar du delningssidan i webbläsaren. Du kan också kopiera länken.

[English README](../README.md) · [Deutsch](../README.de.md)
