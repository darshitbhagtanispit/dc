import Pyro4

def print_options(options):
    for option in options:
        print(option)

def main():
    bank = Pyro4.Proxy("PYRONAME:bank")

    options = bank.get_options()
    while True:
        print_options(options)
        choice = int(input("Enter your choice (1-5): "))

        if choice == 5:
            break

        account_number = input("Enter account number: ")

        if choice in [1, 3, 4]:  # Create, Deposit, or Withdraw
            amount = float(input("Enter amount: "))
            result = bank.execute_option(choice, account_number, amount)
        elif choice == 2:  # Check Balance
            result = bank.execute_option(choice, account_number)
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        print(result)

if __name__ == "__main__":
    main()
