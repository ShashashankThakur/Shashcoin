class Token:
    def __init__(self, initial_supply):
        self.total_supply = initial_supply
        self.balances = {}

    def transfer(self, sender, receiver, amount):
        if sender not in self.balances or self.balances[sender] < amount:
            print("Insufficient balance for transfer.")
            return False

        self.balances[sender] -= amount
        if receiver not in self.balances:
            self.balances[receiver] = amount
        else:
            self.balances[receiver] += amount

        return True

    def get_balance(self, account):
        return self.balances.get(account, 0)

    def mint(self, recipient, amount):
        self.total_supply += amount
        if recipient not in self.balances:
            self.balances[recipient] = amount
        else:
            self.balances[recipient] += amount
