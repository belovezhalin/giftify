# Prezentacja rezultatów projektu

## Kluczowe elementy diagramu klas

Diagram klas ilustruje strukturę aplikacji GiftifyApp oraz jej główne komponenty. Obejmuje:
- **GiftifyApp**: główną klasę uruchamiającą aplikację.
- **ICertificate**: interfejs dla wszystkich certyfikatów.
- **BaseCertificate**: abstrakcyjna klasa bazowa dla certyfikatów.
- **SpaCertificate, CulinaryCertificate, SportsCertificate**: konkretne implementacje certyfikatów.
- **CertificateFactory**: klasa fabryki tworząca certyfikaty.
- **User i ShoppingCart**: zarządzająca użytkownikami i koszykami zakupowymi.
- **Filtry (CityFilter, CategoryFilter, PriceFilter)**: implementacja strategii filtrowania certyfikatów.
- **Zastosowane wzorce projektowe**: Singleton, Factory, Strategy, Observer, Decorator, itp.

## Zastosowane wzorce projektowe i ich uzasadnienie

W projekcie zostały zastosowane różne wzorce projektowe, które mają na celu poprawę organizacji kodu i ułatwienie jego rozwoju:
1. **Factory Method** – pozwala na tworzenie obiektów certyfikatów w sposób elastyczny i łatwy do rozszerzenia.
2. **Singleton** – zapewnia, że w aplikacji istnieje tylko jedna instancja koszyka zakupowego, co pozwala na centralne zarządzanie stanem.
3. **Strategy** – umożliwia zastosowanie różnych metod filtrowania certyfikatów, co ułatwia ich rozszerzanie o nowe filtry.
4. **Observer** – implementuje powiadomienia o nowych ofertach dla użytkowników.
5. **Decorator** – umożliwia dynamiczne dodawanie nowych cech do certyfikatów (np. tagi promocyjne, premium).
6. **Facade** – upraszcza dostęp do różnych funkcji systemu, takich jak wyszukiwanie i filtrowanie certyfikatów.

## Sposób implementacji zasad SOLID w projekcie

Zasady SOLID zostały zastosowane w następujący sposób:
- **S (Single Responsibility Principle)**: Każda klasa i interfejs w projekcie mają jedno, dobrze zdefiniowane zadanie. Na przykład `User` zarządza danymi użytkownika, a `CertificateFactory` odpowiedzialna jest za tworzenie certyfikatów.
- **O (Open/Closed Principle)**: Kod jest otwarty na rozszerzenia (np. nowe typy certyfikatów), ale zamknięty na modyfikacje. Nowe certyfikaty mogą być dodawane poprzez rozszerzenie klas, nie zmieniając istniejącego kodu.
- **L (Liskov Substitution Principle)**: Klasy pochodne (`SpaCertificate`, `CulinaryCertificate`, `SportsCertificate`) mogą być używane zamiast bazowej klasy `BaseCertificate` bez wprowadzania błędów.
- **I (Interface Segregation Principle)**: Zastosowanie małych, dedykowanych interfejsów, takich jak `ICertificate`, aby umożliwić implementację tylko wymaganych metod.
- **D (Dependency Inversion Principle)**: Wysokopoziomowe klasy (np. `ShoppingCart`, `CatalogFacade`) nie zależą od szczegółów implementacji certyfikatów, ale od abstrakcji (`ICertificate`).

## Doświadczenia związane z planowaniem zadań, korzystaniem z PlantUML i GitHub

Planowanie zadań:
- Zastosowałam podejście Agile, tworząc backlog zadań i regularnie je przeglądając.

Korzystanie z PlantUML:
- PlantUML okazał się być bardzo pomocnym narzędziem do wizualizacji struktury aplikacji i projektowania klas.

Korzystanie z GitHub:
- GitHub umożliwił efektywną współpracę nad kodem, umożliwiając łatwe zarządzanie wersjami oraz kodem źródłowym.

## Prezentacja wyników testów

### 1. Liczba i rodzaj napisanych testów jednostkowych

W projekcie napisano łącznie **33 testy jednostkowe**, obejmujących różne komponenty systemu. Rodzaje testów to:

- **Testy funkcjonalne**: Weryfikują poprawność działania funkcji w aplikacji, takich jak dodawanie/usuwanie pozycji z koszyka oraz obliczanie sumy.
- **Testy integracyjne**: Testują integrację różnych komponentów, zapewniając poprawność interakcji między klasami (np. `Cart`, `CartItem`, `Certificate`).
- **Testy wzorców projektowych**: Weryfikują poprawność implementacji wzorców projektowych (np. Singleton, Factory, Observer).
- **Brak implementacji testów przypadków brzegowych**: ze względu na szkieletowy charakter projektu, nie zaimplementowano testów przypadków brzegowych. 

### 2. Poziom pokrycia kodu

Do pomiaru pokrycia kodu użyłam **Coverage.py**. Aktualny poziom pokrycia można zobaczyć w formacie HTML, uruchamiając polecenie: 
   ```bash
   start htmlcov/index.html
   ```

### 3. Przykłady wyników testów

Oto kilka przykładów wyników testów oraz ich znaczenie:

- **Test: `test_add_item`**
  - **Opis**: Weryfikuje, czy pozycja może zostać pomyślnie dodana do koszyka.
  - **Wynik**: Zaliczone
  - **Znaczenie**: Upewnia, że koszyk poprawnie dodaje nowe pozycje, zapewniając integralność zawartości koszyka.

- **Test: `test_calculate_total`**
  - **Opis**: Weryfikuje, czy suma cen pozycji w koszyku jest poprawnie obliczana.
  - **Wynik**: Zaliczone
  - **Znaczenie**: Zapewnia poprawność obliczeń całkowitej ceny, co jest kluczowe dla procesu realizacji zamówienia.

- **Test: `test_remove_item`**
  - **Opis**: Weryfikuje, czy pozycja może zostać pomyślnie usunięta z koszyka.
  - **Wynik**: Nieudane (Przyczyna: Pozycja nie została poprawnie usunięta z powodu błędu w funkcji `remove_item`)
  - **Znaczenie**: Ta nieudana próba testu pomogła zidentyfikować i naprawić błąd w logice usuwania pozycji, co zapewnia prawidłowe działanie koszyka.

### 4. Problemy napotkane podczas testowania i rozwiązania

#### Problem 1: 100% pokrycie testami niektórych metod
- **Problem**: Poziom pokrycia niektórych metod (np. związanych z dekoratorami) jest zbyt wysoki ze względu na niepełną implementację tego wzorcu.
- **Rozwiązanie**: Do issues były dodane uwagi do przyszłej implementacji dekoratora i ewentualne przypadki testowania.

---

## Link do pliku PRESENTATION.md
Wszystkie powyższe informacje zostały zawarte w pliku `PRESENTATION.md`, który znajduje się w naszym repozytorium: [Link do PRESENTATION.md](https://github.com/belovezhalin/Giftify/blob/main/PRESENTATION.md)
