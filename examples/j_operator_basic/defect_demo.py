from topologic.defect import defect


def main():
    # Sygnal ze stabilnym poczatkiem, a potem jednym duzym skokiem (defekt)
    values = [1.0, 1.1, 1.2, 1.3, 3.5, 3.6, 3.7]

    print("=== DEFECT DEMO ===")
    print("(v0.2: defect() potrzebuje 'history' - probek SPRZED prev/curr -")
    print(" zeby policzyc bazowa zmiennosc; bez tego wynik byl matematycznie")
    print(" niezalezny od wielkosci skoku, patrz README sekcja 'Poprawki')")
    for i in range(1, len(values)):
        prev = values[i - 1]
        curr = values[i]
        history = values[max(0, i - 3):i - 1]  # do 3 probek SPRZED prev
        if len(history) < 2:
            print(f"prev={prev:.2f}, curr={curr:.2f} -> za malo historii, pomijam")
            continue
        d = defect(prev, curr, sigma=2.0, history=history)
        print(f"prev={prev:.2f}, curr={curr:.2f}, history={['%.2f' % h for h in history]} -> defect={d}")


if __name__ == "__main__":
    main()
