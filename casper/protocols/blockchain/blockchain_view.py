"""The blockchain view module extends a view for blockchain data structures """
from casper.safety_oracles.clique_oracle import CliqueOracle
from casper.abstract_view import AbstractView


class BlockchainView(AbstractView):
    """A view class that also keeps track of a last_finalized_block and children"""

    def __init__(self, messages=None, genesis_block=None):
        self.children = dict()
        self.last_finalized_block = genesis_block
        self.genesis_block = genesis_block

        self._initialize_message_caches(messages)

        super().__init__(messages)

    def estimate(self):
        """Returns the current forkchoice in this view"""

        # Starts from the last_finalized_block and stops when it reaches a tip.
        scores = dict()

        for validator in self.latest_messages:
            current_block = self.latest_messages[validator]

            while current_block and current_block != self.last_finalized_block:
                scores[current_block] = scores.get(
                    current_block, 0) + validator.weight
                current_block = current_block.estimate

        best_block = self.last_finalized_block
        while best_block in self.children:
            curr_scores = dict()
            max_score = 0
            for child in self.children[best_block]:
                curr_scores[child] = scores.get(child, 0)
                max_score = max(curr_scores[child], max_score)

            # We don't choose weight 0 children.
            # Also possible to make non-deterministic decision here.
            if max_score == 0:
                break

            max_weight_children = self.get_max_weight_indexes(curr_scores)

            assert len(max_weight_children) == 1, "... there should be no ties!"

            best_block = max_weight_children.pop()

        return best_block

    def update_safe_estimates(self, validator_set):
        """Checks safety on messages in views forkchoice, and updates last_finalized_block"""
        tip = self.estimate()

        while tip and tip != self.last_finalized_block:
            oracle = CliqueOracle(tip, self, validator_set)
            fault_tolerance, _ = oracle.check_estimate_safety()

            if fault_tolerance > 0:
                self.last_finalized_block = tip
                self._update_when_finalized_cache(tip)
                return self.last_finalized_block

            tip = tip.estimate

    def _update_protocol_specific_view(self, message):
        """Given a now justified message, updates children and when_recieved"""
        assert message.hash in self.justified_messages, "...should not have seen message!"

        # update the children dictonary with the new message
        if message.estimate not in self.children:
            self.children[message.estimate] = set()
        self.children[message.estimate].add(message)

        self._update_when_added_cache(message)

    def _initialize_message_caches(self, messages):
        self.when_added = {message: 0 for message in messages}
        self.when_finalized = {self.genesis_block: 0}

    def _update_when_added_cache(self, message):
        if message not in self.when_added:
            self.when_added[message] = len(self.justified_messages)

    def _update_when_finalized_cache(self, tip):
        while tip and tip not in self.when_finalized:
            self.when_finalized[tip] = len(self.justified_messages)
            tip = tip.estimate

    def get_max_weight_indexes(self, scores):
        """Returns the keys that map to the max value in a dict.
        The max value must be greater than zero."""

        max_score = max(scores.values())

        assert max_score != 0, "max_score of a block should never be zero"

        max_weight_estimates = {e for e in scores if scores[e] == max_score}

        return max_weight_estimates
