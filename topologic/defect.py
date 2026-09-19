import numpy as np


def defect(prev, curr, sigma=2.0, history=None):
    """
    Operator defektu: wykrywa skok/anomalie miedzy `prev` a `curr`
    WIEKSZY NIZ `sigma` odchylen standardowych BAZOWEJ zmiennosci sygnalu.

    POPRAWKA BLEDU (v0.2): oryginalna wersja liczyla odchylenie standardowe
    z tych samych dwoch punktow, ktore akurat porownywala:
    `np.std([prev, curr])`. Dla dwoch liczb a,b odchylenie standardowe
    (populacyjne) wynosi z definicji |a-b|/2, wiec warunek
    `|curr-prev| > sigma * std([prev,curr])` upraszcza sie algebraicznie
    do stalej `1 > sigma/2`, CALKOWICIE NIEZALEZNEJ od wielkosci skoku.
    Zweryfikowane numerycznie: przy domyslnym sigma=2.0 funkcja NIGDY nie
    zwracala True (nawet dla defect(0.0, 100.0)); przy sigma<2.0 zwracala
    True ZAWSZE, niezaleznie od tego, czy skok byl 0.001 czy 1000 - funkcja
    nie miala zadnej mocy rozrozniajacej.

    Teraz wymaga `history`: listy WCZESNIEJSZYCH wartosci sygnalu
    (SPRZED prev/curr), z ktorej liczona jest baza. Bez realnej historii
    nie da sie statystycznie odroznic anomalii od normalnej zmiennosci -
    zamiast cicho zwracac bezsensowny wynik, funkcja jawnie zglasza
    ValueError.

    Parametry:
      prev, curr - dwie kolejne wartosci sygnalu do porownania
      sigma      - prog czulosci (ile odchylen standardowych)
      history    - lista/sekwencja co najmniej 2 WCZESNIEJSZYCH wartosci
                   sygnalu (nie wliczajac prev/curr), z ktorej liczony
                   jest baseline_std
    """
    if history is None or len(history) < 2:
        raise ValueError(
            "defect() wymaga 'history' (co najmniej 2 wczesniejszych "
            "wartosci sygnalu, SPRZED prev/curr) do policzenia bazowego "
            "odchylenia standardowego - bez tego nie da sie statystycznie "
            "odroznic anomalii od normalnej zmiennosci sygnalu. Przekaz "
            "np. ostatnie N probek PRZED 'prev'."
        )

    baseline_std = float(np.std(np.asarray(history, dtype=float)))
    if baseline_std == 0:
        # historia byla calkowicie plaska - kazda roznica prev/curr jest
        # z definicji anomalia wzgledem tej (zerowej) zmiennosci bazowej
        return curr != prev

    return abs(curr - prev) > sigma * baseline_std
