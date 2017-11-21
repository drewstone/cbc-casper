import copy

from casper.message import Message
from casper.validator import Validator

EMPTY_JUST = dict()

def test_new_message(validator):
    message = Message(None, EMPTY_JUST, validator, 0, 0)

    assert message.sender == validator
    assert message.estimate is None
    assert not any(message.justification)
    assert message.sequence_number == 0


def test_equality_of_copies_off_genesis(validator):
    message = Message(None, EMPTY_JUST, validator, 0, 0)

    shallow_copy = copy.copy(message)
    deep_copy = copy.deepcopy(message)

    assert message == shallow_copy
    assert message == deep_copy
    assert shallow_copy == deep_copy


def test_non_equality_of_copies_off_genesis():
    validator_0 = Validator("v0", 10)
    validator_1 = Validator("v1", 11)

    message_0 = Message(None, EMPTY_JUST, validator_0, 0, 0)
    message_1 = Message(None, EMPTY_JUST, validator_1, 0, 0)

    assert message_0 != message_1
