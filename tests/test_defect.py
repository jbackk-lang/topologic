"""
Testy operatora defect() (v0.2, wymaga 'history').

Regresja: stara wersja liczyla np.std([prev, curr]) - odchylenie
standardowe z tych samych dwoch punktow, ktore akurat porownywala. Dla
dwoch liczb std populacyjne = |a-b|/2, wiec warunek
|curr-prev| > sigma*std([prev,curr]) upraszcza sie do stalej 1 > sigma/2,
CALKOWICIE niezaleznej od wielkosci skoku. Przy sigma=2.0 (domyslne)
funkcja nigdy nie zwracala True - nawet dla defect(0.0, 100.0).
"""
import numpy as np
import pytest

from topologic.defect import defect


def test_raises_without_history():
    with pytest.raises(ValueError):
        defect(1.0, 2.0)


def test_raises_with_insufficient_history():
    with pytest.raises(ValueError):
        defect(1.0, 2.0, history=[1.0])


def test_huge_jump_detected_as_defect_with_stable_history():
    # Stara wersja: defect(0.0, 100.0) byla ZAWSZE False przy sigma=2.0,
    # niezaleznie od historii (bo w ogole jej nie uzywala).
    stable_history = [55.0, 55.0, 56.0, 54.0]
    assert defect(0.0, 100.0, sigma=2.0, history=stable_history) is True


def test_small_change_within_normal_variability_is_not_defect():
    noisy_history = [10.0, 15.0, 8.0, 12.0, 9.0]
    assert defect(10.0, 10.5, sigma=2.0, history=noisy_history) is False


def test_flat_history_any_change_is_defect():
    flat_history = [5.0, 5.0, 5.0]
    assert defect(5.0, 5.1, history=flat_history) is True
    assert defect(5.0, 5.0, history=flat_history) is False


def test_sanity_matches_manual_std_computation():
    history = [1.0, 2.0, 3.0, 4.0]
    baseline_std = float(np.std(history))
    prev, curr = 10.0, 10.0 + 3 * baseline_std
    assert defect(prev, curr, sigma=2.0, history=history) is True
    assert defect(prev, prev + 0.1 * baseline_std, sigma=2.0, history=history) is False
