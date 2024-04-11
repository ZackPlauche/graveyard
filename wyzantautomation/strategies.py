from models import Strategy

from settings import MIN_RATE


class StrategyList(list):

    def __init__(self, *args, **kwargs):
        # Ensure only strategies are entered.
        for strategy in self:
            assert isinstance(strategy, Strategy), f'Expected Strategy, got {type(strategy)}'
        super().__init__(*args, **kwargs)
        self.current_strategy: Strategy | None = None

    def __getitem__(self, index):
        if isinstance(index, str):
            return self.get_strategy(index)
        return super().__getitem__(index)
    
    def __setitem__(self, index, value):
        if isinstance(index, str):
            index = self.index(self.get_strategy(index))
        super().__setitem__(index, value)

    def rotate(self) -> Strategy:
        """Rotate to the next strategy in the list."""
        if self.current_strategy is None:
            self.current_strategy = self[0]
        else:
            index = self.index(self.current_strategy)
            if index + 1 >= len(self):
                self.current_strategy = self[0]
            else:
                self.current_strategy = self[index + 1]
        return self.current_strategy

    def get_strategy(self, name: str) -> Strategy:
        """Get a strategy by name."""
        for strategy in self:
            if strategy.name == name:
                return strategy
        raise ValueError(f'Strategy "{name}" not found.')
    



strategies = StrategyList([
    Strategy(
        name='Default Rate',
        description='Apply using the default rate of your profile wyzant profile.',
        function=lambda job: None,  # Returns None to use default rate.
    ),
    Strategy(
        name='+$20',
        description='Apply with the student\'s recommended rate plus $20.',
        function=lambda job: job.recommended_rate + 20,
    ),
    Strategy(
        name='Minimum Rate',
        description='Apply with a set minimum rate.',
        function=lambda job: MIN_RATE,
    ),
    Strategy(
        name='Professionally Self-Employed',
        description='Apply with the student\'s recommended rate.',
        function=lambda job: job.recommended_rate,
    )
])

