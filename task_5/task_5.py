"""
Задача 5: Определение дня с максимальным количеством гостей в отеле.

Описание:
Дана информация о времени заезда и отъезда посетителей отеля в виде списка кортежей.
Каждый кортеж содержит две строки с датами в формате 'ДД.ММ.ГГ' (например: '15.09.24').
Требуется найти день (включительно), когда в отеле находилось наибольшее
количество гостей одновременно.

Алгоритм:
- Для заезда → событие +1 в день заезда.
- Для отъезда → событие -1 на следующий день после отъезда.
- Сортируем события по дате и сканируем, поддерживая счётчик гостей.
- Отслеживаем день с максимумом.

Теоретическая сложность:
- Время: O(n log n) — из-за сортировки 2n событий.
- Память: O(n) — хранение событий.
"""

from datetime import datetime, timedelta


def parse_date(date_str: str) -> datetime:
    """
    Преобразует строку в формате 'ДД.ММ.ГГ' (например, '15.09.24') в объект datetime.
    Годы 00-68 интерпретируются как 2000-2068, 69-99 → 1969-1999.
    Выбрасывает ValueError при ошибке.
    """
    return datetime.strptime(date_str.strip(), "%d.%m.%y")


def format_date_for_output(dt: datetime) -> str:
    """Форматирует datetime в строку 'ДД.ММ.ГГ'."""
    return dt.strftime("%d.%m.%y")


def max_guests_day(bookings):
    """Возвращает дату (строка в формате 'ДД.ММ.ГГ') с максимальным числом гостей одновременно."""
    if not bookings:
        return None

    events = []
    for arrival, departure in bookings:
        arr_dt = parse_date(arrival)
        dep_dt = parse_date(departure)
        events.append((arr_dt, 1))
        events.append((dep_dt + timedelta(days=1), -1))

    events.sort(key=lambda x: x[0])  # Сортируем только по дате

    current_guests = 0
    max_guests = 0
    best_day = None

    for date, delta in events:
        current_guests += delta
        if current_guests > max_guests:
            max_guests = current_guests
            best_day = date

    return format_date_for_output(best_day) if best_day else None


def input_manual_bookings():
    """Позволяет пользователю ввести количество бронирований, затем ввести их по очереди в формате ДД.ММ.ГГ."""
    while True:
        try:
            n = int(input("Сколько бронирований вы хотите ввести? "))
            if n <= 0:
                print(" Количество должно быть положительным числом.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число (например: 3).")

    bookings = []
    print("\nВведите даты в формате ДД.ММ.ГГ (например: 15.09.24).")

    for i in range(1, n + 1):
        while True:
            print(f"\nБронирование #{i}:")
            arrival = input("  Дата заезда (ДД.ММ.ГГ): ").strip()
            departure = input("  Дата отъезда (ДД.ММ.ГГ): ").strip()

            # Проверка формата дат
            try:
                arr_dt = parse_date(arrival)
                dep_dt = parse_date(departure)
            except ValueError:
                print(" Неверный формат даты. Пример: 15.09.24")
                continue

            # Проверка логики: отъезд не раньше заезда
            if dep_dt < arr_dt:
                print("Дата отъезда не может быть раньше даты заезда. Попробуйте снова.")
                continue

            bookings.append((arrival, departure))
            break  # Успешный ввод — выходим из цикла повтора

    return bookings


def main():
    print(" Задача 5: День с максимальным числом гостей в отеле")
    print("Вы будете вручную ввести данные о бронированиях.\n")

    bookings = input_manual_bookings()

    print("\nВаши бронирования:")
    for i, (a, d) in enumerate(bookings, 1):
        print(f"  {i}. Заезд: {a}, Отъезд: {d}")

    result = max_guests_day(bookings)
    if result:
        print(f"\n День с максимальным числом гостей: {result}")
    else:
        print("\n Невозможно определить день (нет данных).")


if __name__ == "__main__":
    main()