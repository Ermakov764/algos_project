import time
import tracemalloc
from algorithm import build_list, reverse_linked_list, build_list_from_values, list_to_values

def demo_example():
    values = [1, 2, 3, 4, 5]
    head = build_list_from_values(values)
    rev_head = reverse_linked_list(head)
    result = list_to_values(rev_head)
    print(f"Исходный: {values}")
    print(f"Реверс:   {result}")

def measure_reverse(head, n_desc):
    """Измеряет время и память ТОЛЬКО функции reverse_linked_list."""
    tracemalloc.start()
    start_time = time.perf_counter()
    rev_head = reverse_linked_list(head)
    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_taken = end_time - start_time
    print(f"\n--- Замер: время и память реверса ({n_desc}) ---")
    print(f"Время выполнения: {time_taken:.6f} секунд")
    print(f"Память реверса:   {peak_memory} байт")
    print(f"(Это O(1) — не зависит от размера данных)")
    return rev_head

def demo_reversal():
    print("=== Демонстрация реверса ===")
    print("1) Ввести список вручную")
    print("2) Использовать сгенерированный список")
    choice = input("Ваш выбор (1/2): ").strip()
    
    if choice == "1":
        # Ручной ввод
        try:
            inp = input("Числа через пробел: ").strip()
            if not inp:
                print("Пустой ввод. Используем пример [1,2,3,4,5].")
                values = [1, 2, 3, 4, 5]
            else:
                values = list(map(int, inp.split()))
            
            print(f"Исходный: {values}")
            head = build_list_from_values(values)
            rev_head = measure_reverse(head, f"n = {len(values)}")
            result = list_to_values(rev_head)
            print(f"Реверс:   {result}\n")
            
        except Exception as e:
            print(f"Ошибка ввода: {e}. Используем пример.")
            demo_example()
            head = build_list_from_values([1,2,3,4,5])
            measure_reverse(head, "n = 5")
            print()
    
    elif choice == "2":
        # Генерация
        print("\nВыберите размер сгенерированного списка:")
        print("1) 10 элементов")
        print("2) 50 элементов")
        print("3) 100 элементов")
        size_choice = input("Ваш выбор (1/2/3): ").strip()
        size_map = {"1": 10, "2": 50, "3": 100}
        n = size_map.get(size_choice, 10)

        head = build_list(n)
        # Демонстрация
        temp_head = build_list(n)  # для показа результата
        result = list_to_values(reverse_linked_list(temp_head))
        print(f"\nДлина списка: {len(result)}")
        if n <= 20:
            print(f"Результат: {result}")
        else:
            print(f"Начало: {result[:5]} ... Конец: {result[-5:]}")

        # Замер на новом экземпляре
        head_for_measure = build_list(n)
        measure_reverse(head_for_measure, f"n = {n}")
        print()
        
    else:
        print("Неверный выбор. Завершение.\n")

# ==================================================================================
# ТОЧКА ВХОДА
# ==================================================================================
if __name__ == "__main__":
    print("Реверс односвязного списка\n")
    demo_reversal()