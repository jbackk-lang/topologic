"""
Testy operatora resonance() (v0.2, kazdy sygnal jako osobny argument).

Regresja: stara wersja przyjmowala jedna spleszczona liste
resonance([prev_a, curr_a, prev_b, curr_b]) - np.diff na takiej liscie
liczyl m.in. prev_b - curr_a, roznice miedzy dwoma NIEZWIAZANYMI sygnalami,
co psulo wynik. Przyklad z README: A: 1.0->1.3 (rosnie), B: 0.9->1.0
(rosnie) -> stara wersja zwracala False mimo ze oba sygnaly rosna.
"""
import pytest

from topologic.resonance import resonance


def test_single_signal_monotonic_increase_is_resonant():
    assert resonance([1.0, 1.2, 1.5, 1.9]) is True


def test_single_signal_mixed_direction_is_not_resonant():
    assert resonance([1.0, 0.8, 1.1, 0.9]) is False


def test_flat_signal_is_not_resonant():
    assert resonance([1.0, 1.0, 1.0]) is False


def test_two_signals_same_direction_are_resonant():
    # regresja dokladnie z README - stara wersja zwracala False tutaj
    assert resonance([1.0, 1.3], [0.9, 1.0]) is True


def test_two_signals_opposite_direction_are_not_resonant():
    assert resonance([1.0, 1.3], [1.0, 0.7]) is False


def test_multi_signal_all_agree():
    assert resonance([1.0, 1.1, 1.2], [5.0, 5.5, 6.0], [0.1, 0.2, 0.3]) is True


def test_multi_signal_one_disagrees():
    assert resonance([1.0, 1.1, 1.2], [5.0, 5.5, 6.0], [0.3, 0.2, 0.1]) is False


def test_requires_at_least_one_signal():
    with pytest.raises(ValueError):
        resonance()


def test_signal_too_short_raises():
    with pytest.raises(ValueError):
        resonance([1.0])
