from topologic.resonance import resonance


def main():
    # Dwa zestawy wartosci (pojedynczy sygnal):
    # 1) wspolny kierunek (rezonans)
    # 2) mieszany kierunek (brak rezonansu)
    values_resonant = [1.0, 1.2, 1.5, 1.9]
    values_non_resonant = [1.0, 0.8, 1.1, 0.9]

    print("=== RESONANCE DEMO ===")
    r1 = resonance(values_resonant)
    r2 = resonance(values_non_resonant)

    print(f"values_resonant={values_resonant} -> resonance={r1}")
    print(f"values_non_resonant={values_non_resonant} -> resonance={r2}")

    # v0.2: resonance() przyjmuje teraz KAZDY sygnal jako OSOBNY argument,
    # zamiast jednej spleszczonej listy zlaczonej z roznych sygnalow.
    # Przyklad z README, ktory ujawnil blad: A i B oba rosna w tym samym
    # kierunku, ale stara wersja (resonance([prev_a,curr_a,prev_b,curr_b]))
    # zwracala False z powodu sztucznego czlonu miedzysygnalowego
    # (roznica miedzy ostatnia wartoscia A a pierwsza wartoscia B).
    print()
    print("(v0.2: rezonans MIEDZY dwoma sygnalami - kazdy jako osobny")
    print(" argument, nie spleszczona lista)")
    signal_a = [1.0, 1.3]
    signal_b = [0.9, 1.0]
    r3 = resonance(signal_a, signal_b)
    print(f"signal_a={signal_a} (rosnie), signal_b={signal_b} (rosnie) -> resonance={r3}")
    print("(stara wersja zwracala False dla tego przypadku - patrz README)")


if __name__ == "__main__":
    main()
