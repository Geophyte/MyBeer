import javax.swing.*;
import javax.json.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

public class UserWindow extends JFrame {
    private JPanel mainPanel;
    private JTextField usernameField;
    private JTextField emailField;

    UserWindow(JsonObject userObject) {
        setTitle("User Window");
        add(mainPanel);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        pack();
        setResizable(false);
        setVisible(true);

        addWindowListener(new WindowAdapter() {
            @Override
            public void windowDeactivated(WindowEvent e) {
                super.windowDeactivated(e);
                dispose();
            }
        });

        usernameField.setText(userObject.getString("username"));
        emailField.setText(userObject.getString("email"));
    }
}
