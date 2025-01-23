# Prezentacja rezultatów projektu

## Kluczowe elementy diagramu klas

Diagram klas ilustruje strukturę aplikacji Giftify oraz jej główne komponenty. Obejmuje:

- **User**: klasa reprezentująca użytkownika.
- **Customer**: klasa reprezentująca klienta, powiązana z użytkownikiem.
- **Category**: klasa reprezentująca kategorię produktów.
- **Product**: klasa reprezentująca produkt, zawiera informacje takie jak nazwa, cena, kategoria, miejsce, obraz, zniżka i specjalne oznaczenie.
- **Order**: klasa reprezentująca zamówienie, powiązana z klientem, zawiera datę zamówienia, status kompletności i identyfikator transakcji.
- **OrderItem**: klasa reprezentująca pozycję zamówienia, powiązana z produktem i zamówieniem, zawiera ilość i datę dodania.
- **ProductAdmin**: klasa administracyjna dla produktów, zawiera pola do wyświetlania, filtrowania i wyszukiwania.
- **ProductDecorator**: klasa dekoratora dla produktów, umożliwia dodawanie dodatkowych funkcji do produktów.
- **SaleDecorator**: klasa dekoratora dla produktów, dodaje zniżkę i cenę promocyjną.
- **SpecialOccasionDecorator**: klasa dekoratora dla produktów, dodaje specjalne oznaczenie okazji.
- **Observer**: interfejs dla obserwatorów, zawiera metodę `update`.
- **Subject**: klasa podmiotu, zarządza listą obserwatorów i powiadamia ich o zmianach.
- **UserObserver**: klasa obserwatora dla użytkowników, implementuje metodę `update`.
- **Views**: klasa widoków, zawiera metody do obsługi różnych widoków aplikacji, takich jak rejestracja, lista produktów, szczegóły produktu, koszyk, zamówienie i aktualizacja pozycji.
- **Zastosowane wzorce projektowe**: Template Method, Factory, Strategy, Observer, Decorator, Registry, MVT.

## Zastosowane wzorce projektowe i ich uzasadnienie

W projekcie zastosowano różnorodne wzorce projektowe, które zwiększają czytelność kodu, jego modularność oraz ułatwiają rozwój aplikacji:

1. **Strategy** – umożliwia elastyczne zarządzanie różnymi algorytmami, np. w `cart.js` dla obsługi zalogowanych i niezalogowanych użytkowników. Dzięki temu wzorzec ułatwia rozszerzanie i modyfikowanie funkcjonalności bez zmian w kodzie klienta.

2. **Template Method** – wykorzystany w systemie szablonów Django, pozwala na tworzenie bazowych szablonów (np. `store/main.html`), które mogą być rozszerzane przez inne szablony (np. `cart.html`). Zapewnia to spójność interfejsu i efektywne ponowne użycie kodu.

3. **Registry** – stosowany w `admin.py`, umożliwia centralne rejestrowanie modeli w panelu administracyjnym Django, co ułatwia zarządzanie strukturą danych i ich widocznością w systemie.

4. **Decorator** – pozwala dynamicznie dodawać nowe funkcje do istniejących elementów kodu. W `decorators.py` umożliwia np. rozszerzanie zachowań funkcji bez zmiany ich pierwotnej implementacji.

5. **Factory** – funkcja `cookieCart` w `utils.py` działa jako prosty wzorzec fabryki, umożliwiający tworzenie obiektów koszyka zakupowego na podstawie danych przechowywanych w cookies. Dzięki temu logika tworzenia obiektów jest odseparowana i bardziej przejrzysta.

6. **Observer** – zastosowany w systemie powiadomień o nowych ofertach dla użytkowników. Mechanizm ten pozwala na automatyczne informowanie zarejestrowanych użytkowników (obserwatorów) o aktualizacjach, co zwiększa interaktywność i użyteczność aplikacji.

7. **Model-View-Template (MVT)** – architektura używana w Django, która zapewnia wyraźny podział odpowiedzialności między warstwami modelu, logiki biznesowej oraz prezentacji. Ułatwia to organizację kodu i jego rozwój.

Zastosowanie tych wzorców pozwoliło na stworzenie elastycznej, skalowalnej i łatwej w utrzymaniu aplikacji.

## Doświadczenia związane z planowaniem zadań, korzystaniem z PlantUML i GitHub

Planowanie zadań:

- Zastosowałam podejście Agile, tworząc backlog zadań i regularnie je przeglądając.

Korzystanie z PlantUML:

- PlantUML okazał się być bardzo pomocnym narzędziem do wizualizacji struktury aplikacji i projektowania klas.

Korzystanie z GitHub:

- GitHub umożliwił efektywną współpracę nad kodem, umożliwiając łatwe zarządzanie wersjami oraz kodem źródłowym.

## Prezentacja wyników testów

### 1. Liczba i rodzaj napisanych testów jednostkowych

W projekcie napisano łącznie **16 testów jednostkowych**, obejmujących różne komponenty systemu. Rodzaje testów to:

- **Testy funkcjonalne**: Weryfikują poprawność działania funkcji w aplikacji, takich jak dodawanie/usuwanie pozycji z koszyka oraz obliczanie sumy.
- **Testy integracyjne**: Testują integrację różnych komponentów, zapewniając poprawność interakcji między klasami (np. `Order`, `OrderItem`, `Product`).
- **Testy wzorców projektowych**: Weryfikują poprawność implementacji wzorców projektowych (np. Singleton, Observer).
- **Brak implementacji testów przypadków brzegowych**: nie zaimplementowano testów przypadków brzegowych.

### 2. Poziom pokrycia kodu

Do pomiaru pokrycia kodu użyłam **Coverage.py**. Aktualny poziom pokrycia można zobaczyć w formacie HTML, uruchamiając polecenie:

```bash
start htmlcov/index.html
```

### 3. Przykłady wyników testów

Oto kilka przykładów wyników testów oraz ich znaczenie:

- **Test: `test_store_view`**

  - **Opis**: Weryfikuje, czy strona sklepu ładuje się poprawnie i wyświetla produkt.
  - **Wynik**: Zaliczone
  - **Znaczenie**: Upewnia, że strona sklepu jest dostępna i poprawnie wyświetla produkty, co jest kluczowe dla doświadczenia użytkownika.

- **Test: `test_store_view_with_filters`**

  - **Opis**: Weryfikuje, czy strona sklepu poprawnie filtruje produkty na podstawie kategorii, ceny i lokalizacji.
  - **Wynik**: Zaliczone

- **Test: `test_register_view_invalid`**

  - **Opis**: Testuje widok rejestracji z nieprawidłowymi danymi, upewniając się, że użytkownik nie zostanie utworzony i strona pozostanie na tym samym miejscu.
  - **Wynik**: Zaliczone
  - **Znaczenie**: Zapewnia, że system poprawnie obsługuje błędne dane wejściowe podczas rejestracji, co poprawia bezpieczeństwo i użyteczność aplikacji.

- **Test: `test_login_view`**

  - **Opis**: Testuje widok logowania, sprawdzając, czy użytkownik jest poprawnie przekierowywany po pomyślnym logowaniu.
  - **Wynik**: Zaliczone
  - **Znaczenie**: Upewnia się, że proces logowania działa prawidłowo, co jest kluczowe dla dostępu użytkowników do aplikacji.

### 4. Problemy napotkane podczas testowania i rozwiązania

#### Problem 1: Testowanie wzorca Observer

- **Problem**: Testowanie wzorca Observer okazało się trudne ze względu na asynchroniczny charakter powiadomień oraz konieczność symulowania różnych stanów obserwowanych obiektów.
- **Rozwiązanie**: Dodano dodatkowe testy jednostkowe i integracyjne, które symulują różne scenariusze użycia wzorca Observer, aby upewnić się, że wszystkie powiadomienia są wysyłane i odbierane poprawnie. W przyszłości planowane jest również wdrożenie bardziej zaawansowanych narzędzi do testowania asynchronicznego kodu.

---

## Link do pliku PRESENTATION.md

Wszystkie powyższe informacje zostały zawarte w pliku `PRESENTATION.md`, który znajduje się w naszym repozytorium: [Link do PRESENTATION.md](https://github.com/belovezhalin/Giftify/blob/main/PRESENTATION.md)
