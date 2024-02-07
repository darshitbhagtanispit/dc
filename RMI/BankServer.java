
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;



public class BankServer extends UnicastRemoteObject implements Bank {
    private Map<String, Account> accounts;

    public BankServer() throws RemoteException {
        accounts = new HashMap<>();
    }

    @Override
    public void createAccount(String accountNumber, double initialBalance) throws RemoteException {
        accounts.put(accountNumber, new Account(accountNumber, initialBalance));
        System.out.println("Account created: " + accountNumber);
    }

    @Override
    public double getBalance(String accountNumber) throws RemoteException {
        return accounts.getOrDefault(accountNumber, new Account("", 0.0)).getBalance();
    }

    @Override
    public void deposit(String accountNumber, double amount) throws RemoteException {
        Account account = accounts.getOrDefault(accountNumber, new Account("", 0.0));
        account.deposit(amount);
        System.out.println("Deposited " + amount + " into account " + accountNumber);
    }

    @Override
    public void withdraw(String accountNumber, double amount) throws RemoteException {
        Account account = accounts.getOrDefault(accountNumber, new Account("", 0.0));
        if (account.withdraw(amount)) {
            System.out.println("Withdrawn " + amount + " from account " + accountNumber);
        } else {
            System.out.println("Insufficient funds in account " + accountNumber);
        }
    }

    public static void main(String[] args) {
        try {
            // Create and export the bank server
            BankServer bankServer = new BankServer();
            Naming.rebind("BankServer", bankServer);

            System.out.println("Bank Server is running...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
