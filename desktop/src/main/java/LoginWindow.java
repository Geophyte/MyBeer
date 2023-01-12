import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import javax.json.*;
import javax.swing.*;

import java.io.StringReader;
import java.util.*;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

/**
 * LoginWindow is a class that extends JFrame, it is used for creating a GUI for logging in and signing up.
 * It has various fields for logging in and signing up
*/
public class LoginWindow extends JFrame {
    private JPanel mainPanel;
    private JLabel logoField;
    private JButton logInButton;
    private JTextField loginUsernameField;
    private JPasswordField loginPasswordField;
    private JButton signUpButton;
    private JTextField signupUsernameField;
    private JPasswordField signupPasswordField;
    private JPasswordField signupConfPasswordField;
    private JTextField signupEMailField;
    private JTextField signupLastNameField;
    private JTextField signupFirstNameField;

    LoginWindow() {
        // setup logo
        logoField.setIcon(new ImageIcon("beer100x100.png"));

        setTitle("Login Window");
        add(mainPanel);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        pack();
        setResizable(false);
        setVisible(true);

        initSignupFields();
        initLoginFields();

        // setup sign up button
        signUpButton.addActionListener(e->{
            signup();
        });

        // set up log in button
        logInButton.addActionListener(e->{
            login();
        });

        loginUsernameField.requestFocus();
    }

    /**
     * This method initializes the signup fields by adding action listeners to them.
     * It sets up the flow of focus between the fields so that when the user presses enter,
     * focus is moved to the next field. The last field, signupConfPasswordField, triggers the signup() method when enter is pressed.
     */
    private void initSignupFields() {
        signupFirstNameField.addActionListener(e->{
            signupLastNameField.requestFocus();
        });
        signupLastNameField.addActionListener(e->{
            signupEMailField.requestFocus();
        });
        signupEMailField.addActionListener(e->{
            signupUsernameField.requestFocus();
        });
        signupUsernameField.addActionListener(e->{
            signupPasswordField.requestFocus();
        });
        signupPasswordField.addActionListener(e->{
            signupConfPasswordField.requestFocus();
        });
        signupConfPasswordField.addActionListener(e->{
            signup();
        });
    }

    /**
     * Initializes the login fields by adding action listeners to the loginUsernameField and loginPasswordField
     * When the user presses the enter key on the loginUsernameField, the focus is set to the loginPasswordField
     * When the user presses the enter key on the loginPasswordField, the login() method is called
     */
    private void initLoginFields() {
        loginUsernameField.addActionListener(e->{
            loginPasswordField.requestFocus();
        });

        loginPasswordField.addActionListener(e->{
            login();
        });
    }

    /**
     * This method is used to handle signup process. It collects information from signup fields,
     * verifies that the passwords match and sends a request to the backend. If the request is successful,
     * it clears the signup fields and shows an information message. If it's not, it shows an error message.
     */
    private void signup() {
        String firstName = signupFirstNameField.getText();
        String lastName = signupLastNameField.getText();
        String email = signupEMailField.getText();
        String username = signupUsernameField.getText();
        String password = String.valueOf(signupPasswordField.getPassword());
        String confPassword = String.valueOf(signupConfPasswordField.getPassword());

        if(!password.equals(confPassword)) {
            JOptionPane.showMessageDialog(null, "Passwords are not the same", "Error", ERROR_MESSAGE);
            return;
        }

        List<NameValuePair> params = new ArrayList<>();
        params.add(new BasicNameValuePair("first_name", firstName));
        params.add(new BasicNameValuePair("last_name", lastName));
        params.add(new BasicNameValuePair("email", email));
        params.add(new BasicNameValuePair("username", username));
        params.add(new BasicNameValuePair("password", password));

        if (Backend.post(Backend.signupURL, params) != null) {
            signupFirstNameField.setText("");
            signupLastNameField.setText("");
            signupEMailField.setText("");
            signupUsernameField.setText("");
            signupPasswordField.setText("");
            signupConfPasswordField.setText("");
            JOptionPane.showMessageDialog(null, "Sign up successful", "Success", JOptionPane.INFORMATION_MESSAGE);
        } else {
            JOptionPane.showMessageDialog(null, "Sign up failure", "Error", ERROR_MESSAGE);
        }
    }

    /**
     * login method which logs in the user by sending request to the backend with provided username and password.
     * If the response is not null it shows successful log in message and opens new MyBeerForm window and closes the current login window.
     * If the response is null it shows error message and clears the password field.
     */
    private void login() {
        String username = loginUsernameField.getText();
        String password = String.valueOf(loginPasswordField.getPassword());

        List<NameValuePair> params = new ArrayList<>();
        params.add(new BasicNameValuePair("username", username));
        params.add(new BasicNameValuePair("password", password));

        String responseString = Backend.post(Backend.loginURL, params);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonObject responseJson = reader.readObject();
            String token = responseJson.getString("token");
            JOptionPane.showMessageDialog(null, "Log in successful", "Success", JOptionPane.INFORMATION_MESSAGE);
            new MyBeerForm(token);
            setDefaultCloseOperation(DISPOSE_ON_CLOSE);
            dispose();
        } else {
            JOptionPane.showMessageDialog(null, "Log in failure", "Error", ERROR_MESSAGE);
            loginPasswordField.setText("");
        }
    }
}
