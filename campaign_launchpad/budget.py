
class GlobalBudget:
    """
    One shared marketing budget across the system.
    """
    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
        # Singleton: the first call creates and funds the wallet, every later
        # call hands back that same object and ignores the amount.
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._balance = float(initial_amount)
            cls._instance = instance
        return cls._instance

    def allocate(self, amount: float) -> None:
        # Allocate amount from the budget
        if amount <= 0:
            raise ValueError("Allocation must be a positive amount")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: tried to allocate {amount}, "
                f"only {self._balance} remaining"
            )
        self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"
