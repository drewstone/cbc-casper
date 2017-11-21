"""The message module defines an abstract message class  """
import random as r


class Message(object):
    """Message/bet data structure for blockchain consensus"""
    def __eq__(self, message):
        if message is None:
            return False
        return self.header == message.header


    def __ne__(self, message):
        return not self.__eq__(message)

    def __init__(self, estimate, justification, sender, sequence_number, display_height):
        assert isinstance(justification, dict), "expected justification a Justification!"

        self.sender = sender
        self.estimate = estimate
        self.justification = justification
        self.sequence_number = sequence_number
        self.display_height = display_height
        self.header = r.random()

    def __hash__(self):
        # NOTE: This does not work once validators have the ability to equivocate!
        return hash(str(self.header))

    def conflicts_with(self, message):
        '''Must be implemented by child class'''
        raise NotImplementedError
