"""The message module defines an abstract message class  """
import random as r


class Message(object):
    """Message/bet data structure for blockchain consensus"""
    def __init__(self, estimate, justification, sender, sequence_number, display_height):
        assert isinstance(justification, dict), "expected justification a Justification!"

        self.sender = sender
        self.estimate = estimate
        self.justification = justification
        self.sequence_number = sequence_number
        self.display_height = display_height
        self.header = r.random()

    def __hash__(self):
        # defined differently than self.hash to avoid confusion with builtin
        # use of __hash__ in dictionaries, sets, etc
        return hash(self.hash)

    @staticmethod
    def is_message(message):
        if message is None:
            return False
        return isinstance(message, Message)

    def __eq__(self, message):
        if not self.is_message(message):
            return False
        return self.hash == message.hash

    def __lt__(self, message):
        if not self.is_message(message):
            return False
        return self.hash < message.hash

    def __le__(self, message):
        if not self.is_message(message):
            return False
        return self.hash <= message.hash

    def __gt__(self, message):
        if not self.is_message(message):
            return False
        return self.hash > message.hash

    def __ge__(self, message):
        if not self.is_message(message):
            return False
        return self.hash >= message.hash

    @property
    def hash(self):
        return hash(str(self.header))

    def conflicts_with(self, message):
        '''Must be implemented by child class'''
        raise NotImplementedError
