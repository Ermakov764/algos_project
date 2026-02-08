# task_6.py
# Алгоритм Беллмана–Форда с пошаговой визуализацией
#
# Теоретическая сложность по времени: O(V * E)
# Сложность по памяти: O(V)
# Поддерживает отрицательные веса и обнаружение отрицательных циклов.

from typing import List, Tuple, Optional

def bellman_ford_verbose(
    n: int,
    edges: List[Tuple[int, int, float]],
    source: int
) -> Tuple[Optional[List[float]], Optional[List[int]]]:
    """Алгоритм Беллмана–Форда с подробным выводом каждого шага."""
    INF = float('inf')
    dist = [INF] * n
    pred = [-1] * n
    dist[source] = 0

    print(f"\n Начальные расстояния: {format_distances(dist)}")
    print("Начинаем релаксацию рёбер...\n")

    # Основные V-1 проходов
    for i in range(n - 1):
        updated = False
        print(f"🔹 Проход {i + 1} из {n - 1}:")
        for idx, (u, v, w) in enumerate(edges):
            if dist[u] != INF and dist[u] + w < dist[v]:
                old = dist[v]
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
                print(f"  → Ребро {idx}: ({u} → {v}, вес={w}) улучшает расстояние до {v}: {old} → {dist[v]}")
        if not updated:
            print("  → Нет обновлений. Завершаем досрочно.")
            break
        else:
            print(f"  → Расстояния после прохода {i + 1}: {format_distances(dist)}")
        print()

    # Проверка на отрицательный цикл
    print("Проверка на отрицательный цикл (доп. проход)...")
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            print(f"Ребро ({u} → {v}, вес={w}) всё ещё улучшает путь → отрицательный цикл обнаружен!")
            return None, None
    print("  → Отрицательных циклов не найдено.\n")
    return dist, pred


def format_distances(dist: List[float]) -> str:
    """Преобразует список расстояний в читаемую строку."""
    return "[" + ", ".join("∞" if d == float('inf') else f"{d:g}" for d in dist) + "]"


def safe_input_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Значение должно быть ≥ {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Значение должно быть ≤ {max_val}.")
                continue
            return value
        except ValueError:
            print("Ожидалось целое число. Попробуйте снова.")


def safe_input_edge(prompt: str, n: int) -> Tuple[int, int, float]:
    while True:
        try:
            parts = input(prompt).split()
            if len(parts) != 3:
                print("Нужно ввести: начальная вершина, конечная вершина, вес (например: 0 1 -2.5)")
                continue
            u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
            if not (0 <= u < n) or not (0 <= v < n):
                print(f"Вершины должны быть от 0 до {n-1}.")
                continue
            return u, v, w
        except ValueError:
            print("Формат: два целых числа и одно число (вес). Попробуйте снова.")


def draw_graph(n: int, edges: List[Tuple[int, int, float]]) -> None:
    """Выводит текстовую визуализацию графа."""
    print("\n Ваш граф:")
    print(f"Вершины: {list(range(n))}")
    print("Рёбра (направленные):")
    for i, (u, v, w) in enumerate(edges):
        print(f"  {i}: {u} ──({w})──→ {v}")
    print()


def main() -> None:
    print("Алгоритм Беллмана–Форда с визуализацией")
    print("Находит кратчайшие пути даже при отрицательных весах и ищет отрицательные циклы.\n")

    n = safe_input_int("Введите количество вершин (≥1): ", min_val=1)
    m = safe_input_int("Введите количество рёбер (≥0): ", min_val=0)

    edges = []
    if m > 0:
        print("\nВведите рёбра: каждая строка = <начало> <конец> <вес>")
        print("Пример: 0 1 -2.5 → ребро из 0 в 1 с весом -2.5")
        for i in range(m):
            edges.append(safe_input_edge(f"Ребро {i+1}/{m}: ", n))
        draw_graph(n, edges)
    else:
        print("Граф пуст (нет рёбер).")

    source = safe_input_int(f" Введите стартовую вершину (0–{n-1}): ", min_val=0, max_val=n-1)

    distances, _ = bellman_ford_verbose(n, edges, source)

    print("=" * 60)
    if distances is None:
        print("Граф содержит отрицательный цикл! Кратчайшие пути не определены.")
    else:
        print("Итоговые кратчайшие расстояния:")
        for i in range(n):
            d = "∞ (недостижима)" if distances[i] == float('inf') else f"{distances[i]:g}"
            print(f"  Вершина {i}: {d}")


if __name__ == "__main__":
    main()
    