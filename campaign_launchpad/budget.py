
class GlobalBudget:
    """
    One shared marketing budget across the system.
    """
    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
        if cls._instance is None:
            instance = super().__new__(cls)
            if initial_amount < 0:
                raise ValueError("Initial amount cannot be negative")
            instance._balance = float(initial_amount)
            cls._instance = instance
        return cls._instance

    def allocate(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Allocation must be positive")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: requested {amount}, remaining {self._balance}"
            )
        self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"
