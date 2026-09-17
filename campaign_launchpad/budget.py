
class GlobalBudget:
    """
    One shared marketing budget across the system.
    """
    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
        if cls._instance is None:
            obj = super().__new__(cls)
            obj._balance = float(initial_amount)
            cls._instance = obj
        return cls._instance

    def allocate(self, amount: float) -> None:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Allocation must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds to allocate the requested amount.")
        self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"
