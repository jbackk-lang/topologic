"""
Testy operatora twist() (v0.2, wymaga 3 punktow).

Regresja: stara wersja przyjmowala tylko (prev, curr) i faktycznie liczyla
"czy sygnal zblizyl sie do threshold", a nie "czy kierunek trendu sie
odwrocil" - mimo ze docstring obiecywal to drugie. Bez trzeciego punktu
(prev2) odwrocenie kierunku jest matematycznie niedefiniowalne.
"""
from topologic.twist import twist


def test_no_reversal_when_monotonic_increase():
    # 1.0 -> 1.5 -> 2.0 : caly czas rosnie, brak odwrocenia
    assert twist(1.0, 1.5, 2.0) is False


def test_reversal_detected_up_then_down():
    # 1.5 -> 2.0 (rosnie) -> 1.8 (spada): odwrocenie kierunku
    assert twist(1.5, 2.0, 1.8) is True


def test_reversal_detected_down_then_up():
    assert twist(2.0, 1.0, 1.5) is True


def test_no_reversal_continues_down():
    assert twist(2.0, 1.8, 1.2) is False


def test_threshold_suppresses_small_reversal():
    # odwrocenie kierunku jest, ale wielkosc zmiany nachylenia jest mala
    prev2, prev, curr = 1.0, 1.1, 1.09
    assert twist(prev2, prev, curr, threshold=0.0) is True
    assert twist(prev2, prev, curr, threshold=10.0) is False


def test_zero_delta_is_not_a_twist():
    # brak ruchu w ktoryms kroku -> kierunek niezdefiniowany -> False
    assert twist(1.0, 1.0, 2.0) is False
    assert twist(1.0, 2.0, 2.0) is False


def test_return_type_is_bool():
    assert isinstance(twist(1.0, 1.5, 2.0), bool)
    assert isinstance(twist(1.5, 2.0, 1.8), bool)
