# A message queue for the ... In mars...

from queue import Queue

from settings.constants import MarsBaseEnum

class MessageQueueA(Queue):

    __message_queue = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MessageQueueA.__message_queue is None:
            MessageQueueA()
        return MessageQueueA.__message_queue

    def __init__(self):
        """ Virtually private constructor. """
        if MessageQueueA.__message_queue is not None:
            raise Exception("Can not re-initiate Singleton Message Queue for MarsBaseEnum.A")
        else:
            MessageQueueA.__message_queue = self
