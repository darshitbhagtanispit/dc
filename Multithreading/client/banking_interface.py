# client/banking_interface.py
import sys
sys.path.append('../server')

from transaction_records import TransactionRecorder



def main():
    transaction_recorder = TransactionRecorder()

    while True:
        username = input("Enter your username: ")
        user_id = transaction_recorder.get_user_id(username)
        if user_id is None:
            print("User not found. Creating a new account...")
            transaction_recorder.add_user(username)
            user_id = transaction_recorder.get_user_id(username)

        while True:
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. View Transaction History")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                amount = float(input("Enter the amount to deposit: "))
                transaction_recorder.deposit(user_id, amount)
                print("Deposit successful.")

            elif choice == '2':
                amount = float(input("Enter the amount to withdraw: "))
                if transaction_recorder.withdraw(user_id, amount):
                    print("Withdrawal successful.")
                else:
                    print("Insufficient funds.")

            elif choice == '3':
                balance = transaction_recorder.get_balance(user_id)
                if balance is not None:
                    print("Your balance is:", balance)
                else:
                    print("Error fetching balance.")

            elif choice == '4':
                print("Transaction History:")
                transactions = transaction_recorder.get_transactions(user_id)
                for transaction in transactions:
                    print(transaction[0])

            elif choice == '5':
                print("Exiting...")
                transaction_recorder.close_connection()
                return

            else:
                print("Invalid choice. Please try again.")

            continue_option = input("Do you want to continue? (yes/no): ")
            if continue_option.lower() != 'yes':
                break

if __name__ == "__main__":
    main()
