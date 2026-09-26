"""
Testy klasy J (v0.2, stanowa, strumieniowe .step()).

Regresja: stara wersja bezstanowa J(prev_a,curr_a,prev_b,curr_b) dostawala
tylko jedna pare kolejnych punktow na wywolanie, wiec pod spodem wolala
zdegenerowane twist()/defect() (2-punktowe) i zepsute resonance()
(spleszczona lista). Przyklad z README (oba sygnaly wyraznie rosnace)
dawal {twist: False, defect: False, resonance: False, J: 0.0}.
"""
from topologic.twist import twist
from topologic.defect import defect
from topologic.resonance import resonance
from topologic.j_operator import J


def make_j(**kwargs):
    return J(twist, defect, resonance, **kwargs)


def test_first_step_is_degenerate_but_well_formed():
    j = make_j()
    result = j.step(1.0, 0.9)
    assert result == {"twist": False, "defect": False, "resonance": False, "J": 0.0}


def test_reset_clears_history():
    j = make_j()
    j.step(1.0, 1.0)
    j.step(2.0, 2.0)
    j.reset()
    result = j.step(1.0, 1.0)
    assert result == {"twist": False, "defect": False, "resonance": False, "J": 0.0}


def test_call_is_alias_for_step():
    j = make_j()
    j2 = make_j()
    a = j(1.0, 0.9)
    b = j2.step(1.0, 0.9)
    assert a == b


def test_streamed_rising_signals_are_no_longer_degenerate():
    # Regresja z README: A i B rosnace razem powinny w koncu dac
    # resonance=True i J>0, NIE staly zdegenerowany zestaw {False,False,False,0.0}.
    j = make_j()
    signal_a = [1.0, 1.1, 1.2, 1.3, 1.4]
    signal_b = [0.9, 1.0, 1.1, 1.2, 1.3]

    results = [j.step(a, b) for a, b in zip(signal_a, signal_b)]

    # przynajmniej jeden krok po rozgrzewce wykrywa rezonans
    assert any(r["resonance"] for r in results[1:])
    # nie wszystkie kroki sa plaskim zerem - operator faktycznie reaguje
    assert any(r["J"] > 0.0 for r in results)


def test_j_point_is_mean_of_three_booleans():
    j = make_j()
    j.step(1.0, 1.0)
    j.step(1.0, 1.0)
    j.step(1.0, 1.0)
    result = j.step(1.0, 1.0)
    assert result["J"] in (0.0, 1.0 / 3, 2.0 / 3, 1.0)


def test_window_limits_history_length():
    j = make_j(window=3)
    for v in range(10):
        j.step(float(v), float(v))
    assert len(j._hist_a) <= 3
    assert len(j._hist_b) <= 3


def test_j_defect_method_mad_detects_step_in_trend():
    from topologic import J, defect, resonance, twist
    Jop = J(twist, defect, resonance, window=30, sigma=2.0, defect_method="mad")
    out = None
    for i in range(20):
        out = Jop.step(float(i), float(i))
    assert out["defect"] is False
    out = Jop.step(23.0, 20.0)  # skok +4 w sygnale A przy typowym kroku +1
    assert out["defect"] is True


def test_j_default_defect_method_is_std():
    from topologic import J, defect, resonance, twist
    Jop = J(twist, defect, resonance)
    assert Jop.defect_method == "std"
