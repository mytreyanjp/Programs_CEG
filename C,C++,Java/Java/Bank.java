import javax.swing.*;
import java.awt.event.*;
import java.awt.FlowLayout;

class AccountDetails {
    int accno;
    String name;
    String phno;
    int age;
    String gender;
    String accountType;
    int balanceAmount;

    public AccountDetails(int accno, String name, String phno, int age, String gender, String accountType) {
        this.accno = accno;
        this.name = name;
        this.phno = phno;
        this.age = age;
        this.gender = gender;
        this.accountType = accountType;
        this.balanceAmount = 0;  // Start with zero balance
    }

    public void withdrawAmount(int x) {
        if (x <= balanceAmount) {
            balanceAmount -= x;
        } else {
            throw new IllegalArgumentException("Insufficient balance");
        }
    }

    public void depositAmount(int x) {
        balanceAmount += x;
    }

    public int getBalance() {
        return balanceAmount;
    }
}

public class Bank extends JFrame {
    private final JTextField textField1, textField2, textField3, textField4;
    private final JLabel j, n, phn, age;
    private final JRadioButton m, fe, no;
    private final ButtonGroup bGroup;
    private JComboBox<String> acctype;
    private JButton check, withdraw, deposit, submit;
    private AccountDetails accountDetails;

    public Bank() {
        super("Bank Application");
        setLayout(new FlowLayout());

        j = new JLabel("Account number:");
        add(j);
        textField1 = new JTextField(10);
        add(textField1);
        
        n = new JLabel("Name:");
        add(n);
        textField2 = new JTextField(10);
        add(textField2);
        
        phn = new JLabel("Phone number:");
        add(phn);
        textField3 = new JTextField(10);
        add(textField3);
        
        age = new JLabel("Age:");
        add(age);
        textField4 = new JTextField(10);
        add(textField4);

        m = new JRadioButton("Male");
        fe = new JRadioButton("Female");
        no = new JRadioButton("Neither");
        add(m);
        add(fe);
        add(no);
        
        bGroup = new ButtonGroup();
        bGroup.add(m);
        bGroup.add(fe);
        bGroup.add(no);

        String[] acc = {"Savings", "Current"};
        acctype = new JComboBox<>(acc);
        add(acctype);

        submit = new JButton("Submit");
        add(submit);
        
        check = new JButton("Check Balance");
        add(check);
        
        withdraw = new JButton("Withdraw Amount");
        add(withdraw);
        
        deposit = new JButton("Deposit Amount");
        add(deposit);

        submit.addActionListener(e -> {
            accountDetails = new AccountDetails(
                Integer.parseInt(textField1.getText()), 
                textField2.getText(), 
                textField3.getText(),
                Integer.parseInt(textField4.getText()), 
                m.isSelected() ? "Male" : fe.isSelected() ? "Female" : "Neither", 
                (String) acctype.getSelectedItem()
            );
            JOptionPane.showMessageDialog(null, "Account created with zero balance.");
        });

        check.addActionListener(e -> {
            if (accountDetails != null) {
                int bal = accountDetails.getBalance();
                JOptionPane.showMessageDialog(null, "Your bank balance: " + bal);
            } else {
                JOptionPane.showMessageDialog(null, "Please create an account first.");
            }
        });

        withdraw.addActionListener(e -> {
            if (accountDetails != null) {
                String d = JOptionPane.showInputDialog("Enter amount to withdraw:");
                try {
                    int amount = Integer.parseInt(d);
                    accountDetails.withdrawAmount(amount);
                    JOptionPane.showMessageDialog(null, amount + " has been withdrawn. Current balance: " + accountDetails.getBalance());
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Invalid input. Please enter a number.");
                } catch (IllegalArgumentException ex) {
                    JOptionPane.showMessageDialog(null, ex.getMessage());
                }
            } else {
                JOptionPane.showMessageDialog(null, "Please create an account first.");
            }
        });

        deposit.addActionListener(e -> {
            if (accountDetails != null) {
                String d = JOptionPane.showInputDialog("Enter amount to deposit:");
                try {
                    int amount = Integer.parseInt(d);
                    accountDetails.depositAmount(amount);
                    JOptionPane.showMessageDialog(null, amount + " has been deposited. Current balance: " + accountDetails.getBalance());
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Invalid input. Please enter a number.");
                }
            } else {
                JOptionPane.showMessageDialog(null, "Please create an account first.");
            }
        });
    }

    public static void main(String[] args) {
        Bank b = new Bank();
        b.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        b.setSize(350, 300);
        b.setVisible(true);
    }
}
