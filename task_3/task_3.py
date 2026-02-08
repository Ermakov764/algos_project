
"""
ЗАДАНИЕ 3: Реализация балансировки красно-чёрного дерева (Red-Black Tree)

ЦЕЛЬ:
Реализовать структуру данных "красно-чёрное дерево", которая поддерживает
быстрые операции вставки и автоматически поддерживает себя в сбалансированном состоянии.

ЧТО ТАКОЕ КРАСНО-ЧЁРНОЕ ДЕРЕВО?
Это особый вид двоичного дерева поиска (BST), в котором каждый узел имеет "цвет" — 
красный (RED) или чёрный (BLACK). Благодаря пяти простым правилам дерево
никогда не вырождается в список и гарантирует время работы O(log n) для всех операций.

ПЯТЬ СВОЙСТВ КЧ-ДЕРЕВА:
1. Каждый узел либо КРАСНЫЙ, либо ЧЁРНЫЙ.
2. Корень дерева — ВСЕГДА ЧЁРНЫЙ.
3. Все листья (пустые места) считаются ЧЁРНЫМИ. (В коде — один общий NIL-узел)
4. Красный узел НЕ МОЖЕТ иметь красного родителя. (Нет двух красных подряд!)
5. Любой путь от корня до листа содержит ОДИНАКОВОЕ число чёрных узлов.

ЗАЧЕМ ЭТО НУЖНО?
Без балансировки обычное BST при вставке упорядоченных данных (1,2,3,4...) превращается
в односвязный список, и поиск становится медленным (O(n)). КЧ-дерево этого не допускает.

ТЕОРЕТИЧЕСКАЯ СЛОЖНОСТЬ:
- Время вставки: O(log n) — дерево всегда сбалансировано (высота ≤ 2·log₂(n+1))
- Память: O(n) — хранится n уникальных ключей
- Дополнительно: O(1) памяти на балансировку (итеративный алгоритм, без рекурсии)
"""

from enum import Enum


# 1. ЦВЕТ УЗЛА: КРАСНЫЙ или ЧЁРНЫЙ
class Color(Enum):
    """Перечисление (enum) для цвета узла."""
    RED = True
    BLACK = False

# 2. УЗЕЛ КРАСНО-ЧЁРНОГО ДЕРЕВА
class RBNode:
    """
    Один узел красно-чёрного дерева.
    
    Атрибуты:
        key    — значение (любое число, включая 0 и отрицательные)
        count  — сколько раз этот ключ был вставлен (для дубликатов)
        color  — цвет узла: RED или BLACK
        left   — левый ребёнок
        right  — правый ребёнок
        parent — родитель (нужен для подъёма при балансировке)
    """
    __slots__ = ("key", "count", "color", "left", "right", "parent")
    
    def __init__(self, key, color=Color.RED):
        self.key = key
        self.count = 1
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        color_str = 'R' if self.color == Color.RED else 'B'
        return f"{self.key}({color_str})[{self.count}]"


# 3. КРАСНО-ЧЁРНОЕ ДЕРЕВО — основной класс
class RedBlackTree:
    """Красно-чёрное дерево с поддержкой дубликатов и безопасной балансировкой."""
    
    def __init__(self):
        # Создаём один общий NIL-узел — он заменяет все пустые листья
        self.NIL = RBNode(None, Color.BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL

    def insert(self, key):
        """Вставить ключ. Если уже есть — увеличить счётчик."""
        existing_node = self._search_existing(key)
        if existing_node != self.NIL:
            existing_node.count += 1
            return

        new_node = RBNode(key)
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = self.NIL
        current = self.root
        while current != self.NIL:
            parent = current
            current = current.left if key < current.key else current.right

        new_node.parent = parent
        if parent == self.NIL:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insert(new_node)

    def _search_existing(self, key):
        """Поиск существующего узла по ключу."""
        current = self.root
        while current != self.NIL:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return self.NIL

    def _fix_insert(self, node):
        """
        Балансировка после вставки.
        Используем явные переменные, как описано в документе:
          - node     — текущий обрабатываемый узел
          - parent   — его родитель
          - grandparent — родитель родителя
          - uncle    — дядя (второй ребёнок grandparent)
        """
        while node.parent.color == Color.RED:
            # === Определяем parent и grandparent ===
            parent = node.parent
            grandparent = parent.parent

            if parent == grandparent.left:
                # === Случаи для левой ветви ===
                uncle = grandparent.right

                if uncle.color == Color.RED:
                    # Случай 1: дядя красный → перекраска
                    parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent  # подъём вверх
                else:
                    # Случай 2 и 3: дядя чёрный
                    if node == parent.right:
                        # Случай 2: node — правый ребёнок → левый поворот
                        node = parent
                        self._left_rotate(node)
                        # После поворота обновляем parent и grandparent
                        parent = node.parent
                        grandparent = parent.parent

                    # Случай 3: node — левый ребёнок → правый поворот + перекраска
                    parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self._right_rotate(grandparent)
                    # После поворота node.parent изменился, но нарушение устранено
                    break  # можно выйти, но для единообразия оставим while

            else:
                # === Зеркальные случаи для правой ветви ===
                uncle = grandparent.left

                if uncle.color == Color.RED:
                    # Случай 1 (зеркало)
                    parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent
                else:
                    # Случай 2 и 3 (зеркало)
                    if node == parent.left:
                        # Случай 2 (зеркало): node — левый ребёнок → правый поворот
                        node = parent
                        self._right_rotate(node)
                        parent = node.parent
                        grandparent = parent.parent

                    # Случай 3 (зеркало): node — правый ребёнок → левый поворот + перекраска
                    parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self._left_rotate(grandparent)
                    break

        # Гарантируем, что корень всегда чёрный (свойство 2)
        self.root.color = Color.BLACK

    def _left_rotate(self, x):
        """Левый поворот вокруг узла x."""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        """Правый поворот вокруг узла y."""
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def inorder(self):
        """Возвращает отсортированный список: (ключ, цвет, счётчик)."""
        result = []
        stack = []
        current = self.root
        while stack or current != self.NIL:
            while current != self.NIL:
                stack.append(current)
                current = current.left
            current = stack.pop()
            color_str = 'RED' if current.color == Color.RED else 'BLACK'
            result.append((current.key, color_str, current.count))
            current = current.right
        return result

    def __repr__(self):
        """Красивое строковое представление дерева."""
        nodes = self.inorder()
        if not nodes:
            return "<пустое дерево>"
        return " → ".join(f"{key}({color[0]})[{count}]" for key, color, count in nodes)


# 4. ПРИМЕР ИСПОЛЬЗОВАНИЯ + РУЧНОЙ ВВОД
if __name__ == "__main__":
    tree = RedBlackTree()
    
    print("Красно-чёрное дерево: поддержка дубликатов, 0, отрицательных чисел.")
    print("Введите целые числа по одному. Для завершения введите 'stop'.\n")

    while True:
        try:
            user_input = input("Введите число (или 'stop' для завершения): ").strip()
            if user_input.lower() == 'stop':
                break

            key = int(user_input)
            tree.insert(key)
            print(f" → Текущее дерево: {tree}\n")

        except ValueError:
            print(" Ошибка: введите целое число или 'stop'.\n")
        except KeyboardInterrupt:
            print("\n\nВыход по Ctrl+C.")
            break

    if tree.inorder():
        print("\n Финальное дерево (in-order обход):")
        print(tree)
        
        print("\nПодробный список всех узлов:")
        for key, color, count in tree.inorder():
            print(f"  Ключ: {key:>3}, Цвет: {color:>5}, Количество вставок: {count}")
        
        zero_node = tree._search_existing(0)
        if zero_node != tree.NIL:
            print(f"\n Ключ 0 вставлен {zero_node.count} раз(а).")
    else:
        print("\n Дерево осталось пустым.")