from typing import Iterable

from cogs.model.circular_queue import CircularQueue


class TestCircularQueue(object):
    @staticmethod
    def __make_queue(elements: Iterable[int]) -> CircularQueue[int]:
        queue = CircularQueue()
        for element in elements:
            queue.put(element)

        return queue

    def test_circular_popping_order(self):
        elements = range(5)
        queue = self.__make_queue(elements)

        for _ in range(2):
            for element in elements:
                assert queue.next() == element

    def test_putting_while_popping_order(self):
        elements = range(3)
        queue = self.__make_queue(elements)

        assert queue.next() == 0
        queue.put(8)
        assert queue.next() == 1
        assert queue.next() == 2

        assert queue.next() == 8
        assert queue.next() == 0
