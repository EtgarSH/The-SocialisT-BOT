from queue import Queue

from cogs.model.social_queue import SocialQueue


class TestSocialQueue(object):
    def test_queue(self):
        participant1 = Queue()
        participant1.put(1)
        participant1.put(2)

        participant2 = Queue()
        participant2.put(3)
        participant2.put(4)

        social_queue = SocialQueue()
        social_queue.add_participant_queue(participant1)
        social_queue.add_participant_queue(participant2)

        assert social_queue.next() == 1
        assert social_queue.next() == 3
        assert social_queue.next() == 2
        assert social_queue.next() == 4
