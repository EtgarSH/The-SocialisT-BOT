from typing import TypeVar, Generic, List

T1 = TypeVar("T1")


class CircularQueue(Generic[T1]):
    def __init__(self):
        self.__elements: List[T1] = []
        self.__current_index = 0

    def put(self, item: T1):
        self.__elements.append(item)

    def next(self) -> T1:
        if len(self.__elements) == self.__current_index:
            self.__current_index = 0

        popped_element = self.__elements[self.__current_index]
        self.__current_index += 1

        return popped_element
