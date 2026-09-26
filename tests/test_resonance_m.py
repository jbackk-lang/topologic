"""Testy rezonansu M (v0.3): koincydencja >= 3 flag w tym samym czasie."""
import numpy as np
import pytest

from topologic import resonance, resonance_m


def test_scalar_flags():
    assert resonance_m([True, True, True, False]) is True
    assert resonance_m([True, True, False, False]) is False
    assert resonance_m([True, True], min_count=2) is True


def test_2d_flags_per_time_step():
    flags = np.array([
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
    ], dtype=bool)
    assert resonance_m(flags).tolist() == [True, False, False, True]


def test_invalid_input():
    with pytest.raises(ValueError):
        resonance_m([True], min_count=0)
    with pytest.raises(ValueError):
        resonance_m(np.zeros((2, 2, 2), dtype=bool))


def test_resonance_m_is_not_directional_resonance():
    # Dwa sygnaly rosnace razem: rezonans kierunkowy True,
    # ale bez jednoczesnych anomalii rezonans M jest False.
    assert resonance([1.0, 1.3], [0.9, 1.0]) is True
    assert resonance_m([False, False]) is False
