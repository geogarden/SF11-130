# SF11/130 — PlumBox

Osobny dodatek Home Assistant dla kotła Lazar SmartFire SF11/130 i sterownika ecoMAX 860P4-LZ. Wersja 1.0.0 bazuje na PlumBox 2.8.52 i używa **pyplumio==0.7.3**. Zawiera aktualny panel, schemat, harmonogram, miesięczne czasy pracy, korekty nadmuchu i podajnika oraz ikonę HKS.

## Instalacja

1. W HA: **Ustawienia → Aplikacje / Dodatki → Sklep → ⋮ → Repozytoria**.
2. Dodaj `https://github.com/geogarden/SF11-130`.
3. Zainstaluj **SF11/130 — PlumBox**. HA zbuduje obraz z Dockerfile.
4. W opcjach wybierz `connection_type: tcp`, ustaw `tcp_host` i `tcp_port` według konwertera TCP–RS485. Dla USB wybierz `serial` i odpowiedni port.
5. Ustaw PIN sterowania (`initial_pin`) i uruchom dodatek. Panel otworzysz przez **Otwórz interfejs WWW** (Ingress). Nowa instalacja domyślnie korzysta z symulacji, dopóki nie wybierzesz połączenia.

Konwerter TCP musi przesyłać surową transmisję ecoNET, a nie Modbus TCP. Parametry UART ustaw w samym konwerterze zgodnie z kotłem. Bezpośredni port WWW jest domyślnie wyłączony; można go opcjonalnie przypisać w ustawieniach sieci dodatku.

## Osobna instalacja i dane

Dodatek ma slug `sf11_130`; jego dane nie są automatycznie kopiowane ze starego PlumBox. Stare repozytorium i instalacja pozostają bez zmian. Przed przenoszeniem konfiguracji lub historii wykonaj kopię zapasową. Bazę kopiuj przy zatrzymanych dodatkach.

Podczas przełączania połączenia zatrzymaj stary dodatek przed uruchomieniem nowego z tym samym konwerterem. To zachowuje jednego klienta komunikacji ze sterownikiem.

Panel otwiera się bez osobnego hasła PlumBox; zapis nastaw wymaga PIN-u i potwierdzenia. Sekrety połączenia i dane użytkownika przechowywane są w `/data`, a nie w repozytorium.

## Zmiana biblioteki

PyPlumIO 0.7.3 używa `serial_for_url`: dla TCP `socket://host:port`, a dla USB ścieżki urządzenia. Zachowano kontrolę limitów czasu, ponawianie sesji i sprzątanie zadań. Testy dekodera harmonogramu dostosowano do API 0.7.3.

Testy automatyczne nie zastępują weryfikacji połączenia z fizycznym kotłem.

## Testy lokalne

```sh
cd plumbox
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
node --test tests/frontend_v2.test.cjs
```

Dalsza dokumentacja: [Dokumentacja PlumBox](plumbox/DOCS.md).
