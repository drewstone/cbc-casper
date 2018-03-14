"""The binary view module extends a view for binary data structures """
import random as r
from casper.protocols.integer.integer_view import IntegerView


class BinaryView(IntegerView):
    """A view class that also keeps track of messages about a bit"""
    def __init__(self, messages=None, first_message=None):
        super().__init__(messages)

    def estimate(self):
        zero_weight, one_weight = 0.0, 0.0

        for v in self.latest_messages:
            if self.latest_messages[v].estimate == 0:
                zero_weight += v.weight
            else:
                one_weight += v.weight

        # zero_weight = sum(v.weight for v in self.latest_messages if self.latest_messages[v].estimate == 0)
        # one_weight = sum(v.weight for v in self.latest_messages if self.latest_messages[v].estimate == 1)

        if zero_weight > one_weight:
            return 0
        elif zero_weight < one_weight:
            return 1
        elif zero_weight == 0:
            return r.randint(0, 1)
        else:
            raise Exception("Should be no ties!")
