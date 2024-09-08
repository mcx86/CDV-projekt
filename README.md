# Jakość powietrza w Polsce na podstawie API GIOŚ

Apilkacja przeglądarkowa korzystacja z API GIOŚ (https://powietrze.gios.gov.pl/pjp/content/api) do prezentacji danych na temat jakości powietrza w Polsce.

Stack:

* Panel (https://panel.holoviz.org/)
* Pandas
* Database - Sqlite
* ORM Peewee (http://docs.peewee-orm.com/en/latest/)

UWAGI:
1. Aby uruchomić aplikację należy wykonać polecenie: `panel serve app.py` (wersja minimalna). Aplikację można wywołać także z przełącznikami --autoreload (automatyczne odświeżenie aplikacji po wprowadzeniu zmian) 
i/lub --show (automatyczne otwarcie aplikacji w domyślnej przegądarce), np. `panel serve app.py --autoreload --show`

2. Aby uruchomić testy należy wykonać polecenie: `pytest`

3. Aby odświeżyć bazę danych należy uruchomić skrypt `load_data_sync.py`. Skrypt ten usuwa wszystkie dotychczasowe dane z tabeli i ładuje najnowsze.

Polecenia z punktów 1 i 2 należy wykonywać będąc w katalogu głównym aplikacji.


Live demo dostępne pod adresem: https://delicate-cherry-8738.ploomberapp.io