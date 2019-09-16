from queue import Queue
from .singleton import Singleton

class MessageQueueA(Queue, metaclass=Singleton):
    pass

class MessageQueueB(Queue, metaclass=Singleton):
    pass
