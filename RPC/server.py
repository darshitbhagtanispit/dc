import Pyro4

@Pyro4.expose
class BankServer:
    def __init__(self):
        self.accounts = {}

    def get_options(self):
        return [
            "1. Create Account",
            "2. Check Balance",
            "3. Deposit",
            "4. Withdraw",
            "5. Exit"
        ]

    def execute_option(self, option, account_number=None, amount=None):
        if option == 1:
            return self.create_account(account_number, amount)
        elif option == 2:
            return self.get_balance(account_number)
        elif option == 3:
            return self.deposit(account_number, amount)
        elif option == 4:
            return self.withdraw(account_number, amount)
        elif option == 5:
            return "Exiting"
        else:
            return "Invalid option"

    def create_account(self, account_number, initial_balance):
        self.accounts[account_number] = initial_balance
        print(f"Account {account_number} created with initial balance: {initial_balance}")
        return f"Account {account_number} created with initial balance: {initial_balance}"

    def get_balance(self, account_number):
        balance = self.accounts.get(account_number, "Account not found")
        print(f"Balance for account {account_number}: {balance}")
        return balance

    def deposit(self, account_number, amount):
        if account_number in self.accounts:
            self.accounts[account_number] += amount
            print(f"Deposited {amount} into account {account_number}. New balance: {self.accounts[account_number]}")
            return f"Deposited {amount} into account {account_number}. New balance: {self.accounts[account_number]}"
        else:
            return "Account not found"

    def withdraw(self, account_number, amount):
        if account_number in self.accounts and self.accounts[account_number] >= amount:
            self.accounts[account_number] -= amount
            print(f"Withdrew {amount} from account {account_number}. New balance: {self.accounts[account_number]}")
            return f"Withdrew {amount} from account {account_number}. New balance: {self.accounts[account_number]}"
        else:
            return "Insufficient funds or account not found"


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(BankServer)
    ns.register("bank", uri)

    print("Bank Server is ready.")
    daemon.requestLoop()


if __name__ == "__main__":
    main()
