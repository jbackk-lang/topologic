from topologic.twist import twist
from topologic.defect import defect
from topologic.resonance import resonance
from topologic.j_operator import J


def main():
    print("=== LOGIKAL: Topological Logic Demo ===")
    print("(v0.2: strumieniowe API - patrz README sekcja 'Poprawki v0.2')")

    # Dwa sygnaly A i B
    A = [1.0, 1.3, 1.7, 1.2, 0.8, 0.6]
    B = [0.9, 1.0, 1.4, 1.6, 1.1, 0.7]

    Jop = J(twist, defect, resonance)

    for i, (value_a, value_b) in enumerate(zip(A, B)):
        result = Jop.step(value_a, value_b)

        print(f"\n--- Step {i} ---")
        print(f"A: {value_a:.2f}")
        print(f"B: {value_b:.2f}")
        print(f"twist={result['twist']}, defect={result['defect']}, resonance={result['resonance']}")
        print(f"J-point={result['J']:.3f}")


if __name__ == "__main__":
    main()
