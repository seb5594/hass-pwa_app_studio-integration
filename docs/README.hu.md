# Webalkalmazás telepítése, párosítása és frissítése

## Küldjön irányítópultot valakinek, akit ismer

Példa. Sebastian létrehoz egy webalkalmazást, amely megmutatja a vonatok indulását. A nagybátyja már használja a hivatalos Home Assistant Companion alkalmazást, és hozzáfér a műszerfalhoz. Sebastian elküldi a böngésző linkjét a WhatsApp-n keresztül.

1. A PWA Web-App Studio alkalmazásban nyissa meg az alkalmazást, lépjen az Accessbe, engedélyezze a bejelentkezést a Companion App segítségével, és mentse. Mindkét alkalmazásnak ugyanazt a Home Assistant szervert kell elérnie HTTPS-en keresztül.

2. Vendége megnyitja a WhatsApp hivatkozást a böngészőjében, és a Bejelentkezés a kísérőalkalmazáson keresztül lehetőséget választja. A webalkalmazás megjelenít egy eszközkódot. A vendég szükség esetén lemásolhatja.

3. Koppintson a Home Assistant megnyitása elemre. Győződjön meg arról, hogy az alkalmazás, a fiók és a kód egyezik. Ha a párosítási oldal kódot kér, illessze be vagy írja be a webalkalmazásban látható kódot. Ezután hagyja jóvá a bejelentkezést.

4. Váltson vissza az eredeti böngészőlapra. Automatikusan bejelentkezik. Ha szükséges, érintse meg a Jóváhagyás ellenőrzése lehetőséget. A kód öt percig és egy bejelentkezésig érvényes.

5. iPhone vagy iPad készüléken a telepített példányba való bejelentkezéshez először adja hozzá az oldalt a Safari kezdőképernyőjéhez. Nyissa meg a Kezdőképernyő ikont, és indítsa el ugyanazt a jóváhagyási folyamatot.

## Keresse meg a Stúdiót

Használja az integrációs fogaskereket, majd nyissa meg a Stúdiót a Home Assistant párbeszédpanelen keresztül. Ha gyakran dolgozik az alkalmazásokon, engedélyezze az Oldalsáv panel kapcsoló entitást az integrációs beállításokban, és kapcsolja be, hogy a parancsikon látható maradjon.

Karbantartási műszerfalhoz adjon hozzá egy gombkártyát, amely a /pwa-app-studio címre navigál. Az opcionális Open PWA Designer gomb entitás az aktív rendszergazdai munkamenetben is megnyithatja. Először engedélyezze azt az entitást; A Home Assistant alapértelmezés szerint letiltja.

## Vendég-irányítópult tervezése és frissítése

Például hozzon létre egy irányítópultot a látogatók számára Wi-Fi információs kártyával és teraszvilágítással. A Tartalom alatt válassza ki az egyes kártyákat, és válasszon egy előre beállított értéket, vagy importáljon egy meglévő kártyát. Állítsa be a címet, az entitást vagy a Markdown elemet a vizuális szerkesztővel, és ellenőrizze a telefon előnézetét.

Az Alkalmazás lépésben állítsa az Alkalmazás verzióját 1.1-re, és mentse. Az a vendég, akinek az alkalmazás még nyitva van, frissítési szalaghirdetést lát, amikor az alkalmazás észleli az új verziót. Az Alkalmazás frissítése elemre koppintva újra betölti a nézetet, és megtartja a kezdőképernyő ikonját és a böngésző munkamenetét. Egy később megnyitott alkalmazás csatlakozáskor az aktuális verziót tölti be.

## Megosztás Androidról

Linkmegosztás használata a Stúdióban. A natív párbeszédpanel akkor nyílik meg, amikor az alkalmazás vagy a böngésző biztosítja. Ha a Companion App nem kínál megosztási API-t, nyissa meg a megosztási oldalt a böngészőben. A linket is másolhatod.

[English README](../README.md) · [Deutsch](../README.de.md)
