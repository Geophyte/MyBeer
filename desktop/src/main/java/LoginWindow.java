import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import javax.json.*;
import javax.swing.*;

import java.io.IOException;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.util.*;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

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
    }

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

    private void initLoginFields() {
        loginUsernameField.addActionListener(e->{
            loginPasswordField.requestFocus();
        });

        loginPasswordField.addActionListener(e->{
            login();
        });
    }

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
            JOptionPane.showMessageDialog(null, "Sign up successful", "Success", JOptionPane.INFORMATION_MESSAGE);
        } else {
            JOptionPane.showMessageDialog(null, "Sign up failure", "Error", ERROR_MESSAGE);
        }
    }

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
            setVisible(false);
            new MyBeerForm(token);
        } else {
            JOptionPane.showMessageDialog(null, "Log in failure", "Error", ERROR_MESSAGE);
        }
    }
}
