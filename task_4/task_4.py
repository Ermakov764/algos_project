# Файл: task_4.py
# Задача: Максимальная прибыль при не более чем k сделках
# 
# Теоретическая сложность:
#   - Временная: O(n * k), если k < n // 2; иначе O(n)
#   - Пространственная: O(k)
#
# Подход:
#   Используем динамическое программирование с двумя массивами:
#     - hold[t] — максимальная прибыль, если мы держим акцию в рамках t-й сделки
#     - sold[t] — максимальная прибыль после завершения t сделок (не держим акцию)
#
#   Оптимизация:
#     Если k >= n // 2, то ограничение на сделки несущественно,
#     и задача решается жадно: сумма всех положительных изменений цен.


def max_profit_k_transactions(prices, k):
    """Возвращает максимальную прибыль при не более чем k сделках."""
    if not prices or k == 0:
        return 0

    n = len(prices)
    
    # Жадный режим
    if k >= n // 2:
        profit = 0
        for i in range(1, n):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit

    # DP-массивы
    sold = [0] * (k + 1)
    hold = [-10**9] * (k + 1) 

    for price in prices:
        for t in range(1, k + 1):
            hold[t] = max(hold[t], sold[t - 1] - price)
            sold[t] = max(sold[t], hold[t] + price)

    return sold[k]

def main():
    print("=== Максимальная прибыль при ≤ k сделках ===")
    
    # Ввод массива цен
    while True:
        try:
            prices_input = input("Введите цены акций через пробел (например: 3 2 6 5 0 3): ").strip()
            if not prices_input:
                print(" Массив не может быть пустым. Попробуйте снова.")
                continue
            prices = list(map(int, prices_input.split()))
            if len(prices) == 0:
                raise ValueError
            break
        except ValueError:
            print("Некорректный ввод. Убедитесь, что вы вводите целые числа через пробел.")

    # Ввод k
    while True:
        try:
            k = int(input("Введите максимальное число сделок k (целое неотрицательное число): "))
            if k < 0:
                print(" k должно быть неотрицательным.")
                continue
            break
        except ValueError:
            print(" Некорректный ввод. Введите целое число.")

    # Вычисление и вывод результата
    result = max_profit_k_transactions(prices, k)
    print("\n Результат:")
    print(f"Цены: {prices}")
    print(f"Макс. число сделок: {k}")
    print(f"Максимальная прибыль: {result}")

if __name__ == "__main__":
    main()


