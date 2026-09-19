from topologic.twist import twist


def main():
    # Prosty sygnal: rosnie, potem spada (odwrocenie kierunku przy indeksie 2->3)
    values = [1.0, 1.5, 2.0, 1.8, 1.2, 0.7]
    threshold = 0.0

    print("=== TWIST DEMO ===")
    print("(v0.2: twist() potrzebuje TRZECH kolejnych punktow, zeby wykryc")
    print(" odwrocenie kierunku - z dwoch punktow to niemozliwe)")
    for i in range(2, len(values)):
        prev2, prev, curr = values[i - 2], values[i - 1], values[i]
        t = twist(prev2, prev, curr, threshold=threshold)
        print(f"{prev2:.2f} -> {prev:.2f} -> {curr:.2f}  ->  twist={t}")


if __name__ == "__main__":
    main()
