"""Testy operatora anomaly() (v0.3, mediana + MAD)."""
import numpy as np
import pytest

from topologic.anomaly import anomaly


def test_requires_history():
    with pytest.raises(ValueError):
        anomaly(1.0, [1.0, 2.0])


def test_double_bill_is_anomaly():
    history = [210.0, 205.0, 215.0, 208.0, 212.0, 207.0, 211.0, 209.0, 213.0, 206.0, 214.0, 210.0]
    assert anomaly(420.0, history) is True
    assert anomaly(216.0, history) is False


def test_single_large_value_in_history_does_not_mask_new_anomaly():
    history = [100.0] * 5 + [101.0, 99.0, 100.5, 99.5, 100.0, 1000.0]  # jedna faktura roczna
    # przy sredniej i 2 sigma 150 zl nie odstaje (std zawyzone przez 1000 zl)
    mean, std = np.mean(history), np.std(history)
    assert not (abs(150.0 - mean) > 2 * std)
    # mediana + MAD widzi 150 zl jako anomalie
    assert anomaly(150.0, history) is True


def test_constant_history():
    assert anomaly(5.0, [5.0, 5.0, 5.0]) is False
    assert anomaly(5.1, [5.0, 5.0, 5.0]) is True
