# Zainstaluj, sparuj i zaktualizuj aplikację internetową

## Wyślij dashboard do kogoś, kogo znasz

Przykład. Sebastian tworzy aplikację internetową, która pokazuje odjazdy pociągów. Jego wujek korzysta już z oficjalnej aplikacji Home Assistant Companion i ma dostęp do deski rozdzielczej. Sebastian wysyła link do przeglądarki poprzez WhatsApp.

1. W PWA Web-App Studio otwórz aplikację, przejdź do Access, włącz logowanie za pośrednictwem aplikacji Companion i zapisz. Obie aplikacje muszą łączyć się z tym samym serwerem Home Assistant poprzez HTTPS.

2. Twój gość otwiera łącze WhatsApp w swojej przeglądarce i wybiera opcję Zaloguj się za pośrednictwem aplikacji Companion. Aplikacja internetowa wyświetla kod urządzenia. W razie potrzeby gość może go skopiować.

3. Kliknij Otwórz Home Assistant. Upewnij się, że aplikacja, konto i kod są zgodne. Jeśli strona parowania poprosi o kod, wklej lub wprowadź kod wyświetlony w aplikacji internetowej. Następnie zatwierdź logowanie.

4. Wróć do oryginalnej karty przeglądarki. Loguje się automatycznie. W razie potrzeby dotknij Sprawdź zatwierdzenie. Kod jest ważny przez pięć minut i na jedno logowanie.

5. Na iPhonie lub iPadzie, aby zalogować się do zainstalowanej kopii, najpierw dodaj stronę do ekranu głównego w przeglądarce Safari. Otwórz ikonę na ekranie głównym i rozpocznij tam ten sam proces zatwierdzania.

## Znajdź Studio

Użyj narzędzia integracyjnego, a następnie otwórz Studio w oknie dialogowym Home Assistant. Jeśli często pracujesz nad aplikacjami, włącz opcję przełączania Panelu bocznego w ustawieniach integracji i włącz ją, aby skrót był widoczny.

W przypadku panelu konserwacji dodaj kartę przycisku, która prowadzi do /pwa-app-studio. Opcjonalny przycisk Otwórz projektanta PWA może go również otworzyć w aktywnej sesji administratora. Najpierw włącz tę jednostkę; Home Assistant domyślnie ją wyłącza.

## Zaprojektuj i zaktualizuj panel gościa

Utwórz na przykład pulpit nawigacyjny dla gości z kartą informacyjną Wi-Fi i oświetleniem patio. W obszarze Treść wybierz poszczególne karty i wybierz ustawienie wstępne lub zaimportuj istniejącą kartę. Ustaw tytuł, podmiot lub Markdown za pomocą edytora wizualnego i sprawdź podgląd w telefonie.

W kroku aplikacji ustaw wersję aplikacji na 1.1 i zapisz. Gość, który nadal ma otwartą aplikację, zobaczy baner aktualizacji, gdy aplikacja wykryje nową wersję. Dotknięcie Aktualizuj aplikację powoduje ponowne załadowanie widoku i zachowanie ikony ekranu głównego oraz sesji przeglądarki. Aplikacja otwarta później ładuje aktualną wersję po podłączeniu.

## Udostępnij z Androida

Użyj udostępniania linków w Studio. Natywne okno dialogowe otwiera się, gdy aplikacja lub przeglądarka je udostępnia. Jeśli aplikacja towarzysząca nie udostępnia interfejsu API udostępniania, otwórz stronę udostępniania w przeglądarce. Możesz także skopiować link.

[English README](../README.md) · [Deutsch](../README.de.md)
