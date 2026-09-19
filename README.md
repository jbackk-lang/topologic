# topologic
Topological Logic for Signals: Twist • Defect • Resonance • J‑Operator

## Dokumentacja online
https://jbackk-lang.github.io/

---

## Opis

`topologic` to lekka biblioteka programistyczna, która udostępnia cztery operatory topologiczne do analizy sygnałów:

- **twist** – skręt (odwrócenie kierunku sygnału)
- **defect** – defekt (skok/anomalia względem bazowej zmienności)
- **resonance** – rezonans (wspólny kierunek zmian wielu sygnałów)
- **J‑operator** – operator decyzyjny łączący trzy powyższe, strumieniowo

Projekt inspirowany TIMDR, Λ–τ–ρ oraz topologią przejść (He → Fe → Og).
Celem jest udostępnienie prostych operatorów, które można stosować w:

- analizie sygnałów
- ML
- finansach
- fizyce
- chemii
- biologii

---

## Struktura repozytorium

```
topologic/
    twist.py
    defect.py
    resonance.py
    j_operator.py

examples/
    j_operator_basic/
        twist_demo.py
        defect_demo.py
        resonance_demo.py
        j_point_demo.py
    logikal.py

tests/
    test_twist.py
    test_defect.py
    test_resonance.py
    test_j_operator.py
    test_package.py
```

---

## Instalacja (lokalnie)

```bash
pip install -e .
```

## Przykład użycia (v0.2)

```python
from topologic.twist import twist
from topologic.defect import defect
from topologic.resonance import resonance
from topologic.j_operator import J

A = [1.0, 1.3, 1.7, 1.2]
B = [0.9, 1.0, 1.4, 1.6]

# J jest STANOWY - karmimy go strumieniem probek przez .step()
Jop = J(twist, defect, resonance)

for value_a, value_b in zip(A, B):
    result = Jop.step(value_a, value_b)
    print(result)
```

Wynik (kształt zawsze taki sam, wartości zależą od historii w oknie):

```json
{
  "twist": true,
  "defect": false,
  "resonance": true,
  "J": 0.667
}
```

Surowe funkcje są też dostępne bezpośrednio, jeśli wolisz zarządzać własną historią:

```python
twist(prev2, prev, curr, threshold=0.0)              # potrzebuje 3 punktów
defect(prev, curr, sigma=2.0, history=[...])          # potrzebuje >=2 wcześniejszych próbek
resonance(signal_a, signal_b, ...)                    # każdy sygnał jako osobny argument
```

---

## Poprawki v0.2 (breaking changes)

Audyt biblioteki wykrył trzy błędy matematyczne w wersji 0.1 oraz jeden brak w eksportach. Wszystkie zostały naprawione, kosztem zmiany sygnatur funkcji (stąd bump do v0.2). Konkretne przykłady liczbowe:

**`defect()` był matematycznie zdegenerowany.** Stara wersja liczyła `np.std([prev, curr])` — odchylenie standardowe z tych samych dwóch punktów, które akurat porównywała. Dla dwóch liczb `a, b` odchylenie standardowe (populacyjne) wynosi z definicji `|a-b|/2`, więc warunek `|curr-prev| > sigma * std([prev,curr])` upraszcza się algebraicznie do stałej `1 > sigma/2` — **całkowicie niezależnej od wielkości skoku**. Przy domyślnym `sigma=2.0` funkcja nigdy nie zwracała `True`, nawet dla `defect(0.0, 100.0)`. Teraz `defect()` wymaga jawnego `history` (wcześniejszych próbek sprzed `prev`/`curr`), z którego liczy bazowe odchylenie standardowe — bez historii zgłasza `ValueError` zamiast cicho zwracać bezsensowny wynik.

**`resonance()` był psuty przez sklejanie różnych sygnałów.** Stara wersja przyjmowała jedną spłaszczoną listę, więc wywołanie `resonance([prev_a, curr_a, prev_b, curr_b])` (używane wewnątrz `J`) liczyło `np.diff` na liście zawierającej m.in. `prev_b - curr_a` — różnicę między ostatnią wartością sygnału A a pierwszą wartością sygnału B, wielkość bez sensu fizycznego. Przykład: A rośnie `1.0 → 1.3`, B rośnie `0.9 → 1.0` — stara funkcja zwracała `resonance=False`, mimo że oba sygnały wyraźnie rosną w tym samym kierunku. Teraz każdy sygnał podaje się osobno: `resonance(signal_a, signal_b, ...)`.

**`twist()` nie mógł wykryć tego, co obiecywał docstring.** Stara wersja przyjmowała tylko `(prev, curr)` i liczyła `(curr-prev)*(prev-threshold)<0` — czyli faktycznie "czy sygnał zbliża się do `threshold`", nie "czy kierunek trendu się odwrócił". Odwrócenia kierunku matematycznie nie da się wykryć z dwóch punktów — potrzeba trzeciego, wcześniejszego (`prev2`), żeby w ogóle mieć poprzedni kierunek do porównania. Nowa sygnatura: `twist(prev2, prev, curr, threshold=0.0)`.

**`J` operator był bezstanowy i dziedziczył wszystkie trzy powyższe błędy.** Wywołanie `J(prev_a, curr_a, prev_b, curr_b)` dostawało tylko jedną parę kolejnych punktów, więc pod spodem musiało wołać zdegenerowane 2-punktowe `twist()`/`defect()` i zepsute `resonance()`. Przykład z tego README: oba sygnały A i B wyraźnie rosnące dawały `{twist: False, defect: False, resonance: False, J: 0.0}` — zdegenerowany wynik, mimo oczywistego sygnału w danych. `J` jest teraz klasą stanową: `J.step(value_a, value_b)` przyjmuje jedną nową próbkę na wywołanie i sam trzyma wewnętrzne okno historii (`window`, domyślnie 20 próbek na sygnał), z którego liczy wszystko, co potrzebne. `J(...)` (wywołanie instancji) jest aliasem na `.step()`.

**Brakujący eksport.** `J` nie był wyeksportowany z `topologic/__init__.py` — `from topologic import J` się wywalało. Naprawione, `__all__ = ["twist", "defect", "resonance", "J"]`.

Wszystkie cztery poprawki mają testy regresyjne w `tests/`, odtwarzające dokładnie powyższe przykłady liczbowe.

---

## Kontekst topologiczny (opcjonalny, koncepcyjny)

> **Uwaga:** poniższy pipeline (TRM/TIMDR/GIA/FIELDCORE/SENSCORE) jest opisem koncepcyjnym/inspiracją teoretyczną, a **nie** czymś zaimplementowanym w kodzie tej biblioteki. Faktyczny, zaimplementowany i przetestowany kod to wyłącznie cztery operatory opisane wyżej (`twist`, `defect`, `resonance`, `J`). Sekcja poniżej dokumentuje zamierzony kierunek/inspirację, nie bieżące API.

Poniżej skrót formalnych podstaw — w wersji ASCII, kompatybilnej z GitHubem.

### 1. Przestrzeń topologiczna zdarzenia

```
T = (V, tau)
```
gdzie:
- `V` — zbiór punktów/sygnałów
- `tau` — topologia generowana przez sąsiedztwo grafowe

Najprostsza konstrukcja:
```
tau = { U ⊆ V | for all v_i in U: N(i) ⊆ U }
```

### 2. TRM — operator topologiczny

Buduje graf z danych i indukuje topologię:
```
TRM : X^N → T
```
Własność: małe zmiany w danych → małe zmiany w topologii.

### 3. TIMDR — zwężanie topologii

```
TIMDR : T → T
```
Nowa topologia:
```
tau' = { U ∩ V' | U ∈ tau }
```
Własność:
```
tau' ⊆ tau
```

### 4. GIA — homotopia rezonansowa

Dopasowuje oś rezonansu i filtruje punkty dalekie od niej:
```
r_i = || q_i - (q_i · u) u ||
```
Homotopia deformacyjna:
```
H(lambda, v_i) = p_bar + lambda * (q_i · u) u
```

### 5. FIELDCORE — wygładzanie topologii

Operator Laplace'a na grafie:
```
g = (1 - lambda) f + lambda L f
```
Energia Dirichleta:
```
E(f) = sum_{(i,j) in E} (f_i - f_j)^2
```

### 6. SENSCORE — zmiana metryki

```
d'(v_i, v_j) = d(v_i, v_j) * g_s
```

### 7. Pipeline

```
T = FIELDCORE ∘ GIA ∘ TIMDR ∘ TRM ∘ SENSCORE
```
Własności: monotoniczność, ciągłość, zbieżność.

---

## Licencja
MIT
