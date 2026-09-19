from topologic.twist import twist
from topologic.defect import defect
from topologic.resonance import resonance
from topologic.j_operator import J


def main():
    print("=== J-POINT DEMO ===")
    print("(v0.2: J jest teraz STANOWY - karmimy go strumieniem probek przez")
    print(" .step(), zamiast jednorazowego wywolania z para punktow. Powod:")
    print(" poprawny twist() potrzebuje 3 punktow, a poprawny defect()")
    print(" potrzebuje historii bazowej - z samej pary (prev, curr) nie da")
    print(" sie tego policzyc poprawnie, patrz README sekcja 'Poprawki v0.2')")

    Jop = J(twist, defect, resonance, window=20, sigma=2.0)

    # Dwa sygnaly: A (lekki spadek, potem odbicie), B (stabilny wzrost)
    signal_a = [1.0, 0.9, 0.6, 0.7, 0.9, 1.2]
    signal_b = [0.9, 1.0, 1.1, 1.3, 1.4, 1.6]

    for i, (value_a, value_b) in enumerate(zip(signal_a, signal_b)):
        result = Jop.step(value_a, value_b)
        print(f"step {i}: a={value_a:.2f}, b={value_b:.2f} -> {result}")


if __name__ == "__main__":
    main()
