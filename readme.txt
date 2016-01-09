PROGRAM MINESWEEPER.PY
autor: Lukasz Blaszczyk
modyfikacje: 9 stycznia 2016

1. Wywolanie funkcji:
./minesweeper.py 
Uwaga: moze byc konieczna zmiana sciezki do zainstalowanej dystrybucji
Pythona (musi zawierac pakiet PyQT4). Aktualnie jest: /opt/anaconda/bin/ipython

2. Mozliwosci:
Aplikacja oferuję znaną (i bardzo lubianą! prawda?) grę Saper. Otwarcie aplikacji uruchamia domyślną planszę o wymiarach 9x9 i 10 bomb. Gra rozpoczynana jest zawsze przy pierwszym kliknięciu myszy (zarówno prawego jak i lewego przycisku). Startuje wówczas zegar, który mierzy czas gry. Planszę resetuje przycisk z buźką na środku okna u góry.
Lewy przycisk myszy odsłania pole gry - jeśli na polu jest bomba, to gra się kończy i użytkownik przegrywa, jeśli na polu nie ma bomby, to odsłaniana jest liczba bomb na sąsiednich polach. Prawy przycisk myszy stawia na danym polu flagę - jest to miejsce, w którym przypuszczalnie jest bomba. Flagę można zdjąć ponownie klikając prawym przyciskiem myszy. Na górze okna, po lewej, znajduje się licznik flag znajdujących się aktualnie na planszy.

3. Dodatkowe opcje:
Istnieje możliwość wyboru rozmiaru planszy. Zdefiniowane są 3 podstawowe poziomy (odpowiadające wielkościom planszy i ilościom bomb) oraz można wybrać opcję planszy zdefiniowanej przez użytkownika - użytkownik sam decyduje jaki jest wymiar planszy (minimalna szerokość to 8, minimalna wysokość to 1, liczba bomb musi być mniejsza niż iloczyn szerokości i wysokości i większa niż jeden). Wybór opcji powoduje zresetowanie planszy.

4. Lista najlepszych wyników:
Najlepsze wyniki w grze są zapisywane. Zapisywane są jedynie wyniki w trzech podstawowych kategoriach. Istnieje możliwość wyzerowania tabeli wyników, odpowiedni przycisk znajduje się w danym oknie.

Miłej gry! :-)
