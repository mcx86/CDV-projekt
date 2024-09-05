# Jakość powietrza w Polsce na podstawie API GIOŚ

Apilkacja przeglądarkowa korzystacja z API GIOŚ (https://powietrze.gios.gov.pl/pjp/content/api) do prezentacji danych na temat jakości powietrza w Polsce.

Stack:

* Panel (https://panel.holoviz.org/)
* Pandas
* Database - Sqlite
* ORRM Peewee (http://docs.peewee-orm.com/en/latest/)

UWAGI:
1. Aby uruchomić aplikację należy wywołać polecenie: `panel serve app.py` (wersja minimalna). Aplikację można wywołać także z przełącznikami --autoreload (automatyczne odświeżenie aplikacji po wprowadzeniu zmian) 
i/lub --show (automatyczne otwarcie aplikacji w domyślnej przegądarce), np. `panel serve app.py --autoreload --show`