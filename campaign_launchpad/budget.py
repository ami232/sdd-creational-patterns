class GlobalBudget:
    """
    One shared marketing budget across the system.
    """

    _instance = None

    def __new__(cls, initial_amount: float = 0.0):
        # Singleton: create the object only the first time
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._balance = initial_amount

        return cls._instance

    def allocate(self, amount: float) -> None:
        # Allocation must be positive
        if amount <= 0:
            raise ValueError("Allocation must be positive")

        # Budget cannot go below zero
        if amount > self._balance:
            raise ValueError("Insufficient funds")

        self._balance -= amount

    def remaining(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"<GlobalBudget remaining={self._balance}>"