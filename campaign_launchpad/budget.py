
class GlobalBudget:
    """
    One shared marketing budget across the system.
    """
    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
      if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._balance = initial_amount
      return cls._instance

    def allocate(self, amount: float) -> None:
      if amount <= 0 or self._balance < amount:
        raise ValueError("Insufficient budget")
      self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"
