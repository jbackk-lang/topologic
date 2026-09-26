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


# ---------------------------------------------------------------------------
# v0.3: metody "mad" i "relative" (zalecenia z projektu TIMeDR-MUZ)
# ---------------------------------------------------------------------------

def test_default_method_is_unchanged_std():
    history = [1.0, 2.0, 3.0, 4.0]
    assert defect(10.0, 12.0, history=history) == defect(10.0, 12.0, history=history, method="std")


def test_unknown_method_raises():
    with pytest.raises(ValueError):
        defect(1.0, 2.0, history=[1.0, 2.0, 3.0], method="foo")


def test_std_misses_step_in_trend_but_mad_detects_it():
    # Znane ograniczenie "std": porownuje krok z rozrzutem POZIOMOW.
    # Trend 0..19 ma std ~5.77, wiec skok +4 (typowy krok to +1) nie przekracza 2*std.
    history = [float(i) for i in range(18)]  # 0..17, prev=18 -> curr=22
    assert defect(18.0, 22.0, sigma=2.0, history=history, method="std") is False
    assert defect(18.0, 22.0, sigma=2.0, history=history, method="mad") is True
    # typowy krok +1 w trendzie nie jest defektem
    assert defect(18.0, 19.0, sigma=2.0, history=history, method="mad") is False


def test_mad_is_robust_to_single_earlier_spike():
    rng = np.random.default_rng(0)
    base = list(100.0 + rng.normal(0, 1.0, 30))
    base[10] += 50.0  # jeden wczesniejszy skok zawyza std krokow, ale nie MAD
    history, prev = base[:-1], float(base[-1])
    curr = prev + 8.0
    assert defect(prev, curr, sigma=3.0, history=history, method="mad") is True
    assert defect(prev, curr, sigma=3.0, history=history, method="std") is False


def test_mad_requires_three_history_points():
    with pytest.raises(ValueError):
        defect(1.0, 2.0, history=[1.0, 2.0], method="mad")


def test_mad_constant_steps_any_deviation_is_defect():
    history = [0.0, 1.0, 2.0, 3.0]
    assert defect(3.0, 4.0, history=history, method="mad") is False
    assert defect(3.0, 4.5, history=history, method="mad") is True


def test_relative_bill_price_rise():
    # abonament 89 -> 119 zl: +33.7% > 10%
    assert defect(89.0, 119.0, method="relative", rel_threshold=0.10) is True
    assert defect(89.0, 92.0, method="relative", rel_threshold=0.10) is False


def test_relative_requires_threshold_and_nonzero_prev():
    with pytest.raises(ValueError):
        defect(89.0, 119.0, method="relative")
    with pytest.raises(ValueError):
        defect(0.0, 5.0, method="relative", rel_threshold=0.10)
