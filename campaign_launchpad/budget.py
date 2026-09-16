
class GlobalBudget:
    """
    One shared marketing budget across the system.
    """
    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
        # Singleton: the first call builds and seeds the shared instance.
        # Later calls hand back that same object and ignore initial_amount,
        # so an existing balance is never silently reset.
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._balance = float(initial_amount)
            cls._instance = instance
        return cls._instance

    def allocate(self, amount: float) -> None:
        # Allocate amount from the budget.
        if amount <= 0:
            raise ValueError(f"Allocation must be positive, got {amount}.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: tried to allocate {amount} "
                f"but only {self._balance} remains."
            )
        self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"
