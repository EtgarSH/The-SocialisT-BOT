from queue import Queue
from typing import TypeVar, Generic

from cogs.model.circular_queue import CircularQueue

T1 = TypeVar("T1")


class SocialQueue(Generic[T1]):
    def __init__(self):
        self.__participant_queues: CircularQueue[Queue[T1]] = CircularQueue()

    def add_participant_queue(self, participant: 'Queue[T1]'):
        self.__participant_queues.put(participant)

    def next(self) -> T1:
        current_participant = self.__participant_queues.next()
        if current_participant.empty():
            return self.next()

        return current_participant.get()
