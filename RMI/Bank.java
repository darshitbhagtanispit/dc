
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Bank extends Remote {
    void createAccount(String accountNumber, double initialBalance) throws RemoteException;
    double getBalance(String accountNumber) throws RemoteException;
    void deposit(String accountNumber, double amount) throws RemoteException;
    void withdraw(String accountNumber, double amount) throws RemoteException;
}
