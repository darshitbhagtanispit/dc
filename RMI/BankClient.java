
import java.rmi.Naming;
import java.util.Scanner;

public class BankClient {
    public static void main(String[] args) {
        try {
            // Lookup the remote bank object
            Bank bank = (Bank) Naming.lookup("BankServer");

            // Create a new account
            bank.createAccount("12345", 1000);

            try (// Perform transactions
            Scanner scanner = new Scanner(System.in)) {
                while (true) {
                    System.out.println("1. Get Balance");
                    System.out.println("2. Deposit");
                    System.out.println("3. Withdraw");
                    System.out.println("4. Exit");
                    System.out.print("Enter your choice: ");

                    int choice = scanner.nextInt();
                    scanner.nextLine(); // Consume the newline character

                    switch (choice) {
                        case 1:
                            System.out.print("Enter account number: ");
                            String accNum = scanner.nextLine();
                            double balance = bank.getBalance(accNum);
                            System.out.println("Balance: " + balance);
                            break;
                        case 2:
                            System.out.print("Enter account number: ");
                            String accNumDeposit = scanner.nextLine();
                            System.out.print("Enter deposit amount: ");
                            double depositAmount = scanner.nextDouble();
                            bank.deposit(accNumDeposit, depositAmount);
                            break;
                        case 3:
                            System.out.print("Enter account number: ");
                            String accNumWithdraw = scanner.nextLine();
                            System.out.print("Enter withdrawal amount: ");
                            double withdrawAmount = scanner.nextDouble();
                            bank.withdraw(accNumWithdraw, withdrawAmount);
                            break;
                        case 4:
                            System.out.println("Exiting...");
                            System.exit(0);
                            break;
                        default:
                            System.out.println("Invalid choice. Please try again.");
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
