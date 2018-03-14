"""The integer view module extends a view for integer data structures """
from casper.safety_oracles.clique_oracle import CliqueOracle
from casper.abstract_view import AbstractView


class IntegerView(AbstractView):
    """A view class for integer values that also keeps track of a last_finalized_estimate"""

    def __init__(self, messages=None, first_message=None):
        super().__init__(messages)

        self.last_finalized_estimate = None

    def estimate(self):
        """Returns the current forkchoice in this view"""
        sorted_bets = sorted(self.latest_messages.values(),
                             key=lambda bet: bet.estimate)
        half_seen_weight = sum(v.weight for v in self.latest_messages) / 2.0

        assert half_seen_weight > 0

        total_estimate_weight = 0
        for bet in sorted_bets:
            total_estimate_weight += bet.sender.weight
            if total_estimate_weight >= half_seen_weight:
                return bet.estimate

    def update_safe_estimates(self, validator_set):
        """Checks safety on most recent created by this view"""
        # check estimate safety on the most
        for bet in self.latest_messages.values():
            oracle = CliqueOracle(bet, self, validator_set)
            fault_tolerance, _ = oracle.check_estimate_safety()

            if fault_tolerance > 0:
                if self.last_finalized_estimate:
                    assert not self.last_finalized_estimate.conflicts_with(bet)
                self.last_finalized_estimate = bet
                break
