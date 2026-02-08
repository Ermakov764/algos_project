# task_1/algorithm.py

class ListNode:
    """Узел односвязного списка."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    """
    Реверс односвязного списка методом трёх указателей.
    Время: O(n), дополнительная память: O(1).
    """
    prev = None
    current = head
    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev

def build_list(n):
    """Создаёт список 1 -> 2 -> ... -> n."""
    if n <= 0:
        return None
    head = ListNode(1)
    current = head
    for i in range(2, n + 1):
        current.next = ListNode(i)
        current = current.next
    return head

def build_list_from_values(values):
    """Создаёт список из Python-списка."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head

def list_to_values(head):
    """Преобразует односвязный список в обычный список."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result