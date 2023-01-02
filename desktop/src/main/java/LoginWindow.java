import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

public class LoginWindow {
    private JPanel mainPanel;
    private JTextField userField;
    private JPasswordField passwordField;
    private JButton logInButton;
    private JButton signUpButton;
    private JLabel logoField;
    private JFrame frame;

    LoginWindow() throws FileNotFoundException {
        // setup logo
        logoField.setIcon(new ImageIcon("beer100x100.png"));

        frame = new JFrame("Login Window");
        frame.add(mainPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setResizable(false);
        frame.setVisible(true);

        // Load users data
        InputStream fis = new FileInputStream("users.json");
        JsonReader reader = Json.createReader(fis);
        JsonArray data = reader.readArray();
        reader.close();

        // setup log in button
        logInButton.addActionListener(e->{
            String login = userField.getText();
            String password = String.valueOf(passwordField.getPassword());

            for(int i=0; i<data.size(); i++) {
                JsonObject userObject = data.getJsonObject(i);
                if(userObject.getString("login").equals(login)) {
                    if(userObject.getString("password").equals(password)) {
                        frame.setVisible(false);

                        // Create main app window
                        try {
                            new MyBeerForm(login);
                        } catch (FileNotFoundException ex) {
                            throw new RuntimeException(ex);
                        }
                    }
                    return;
                }
            }
            JOptionPane.showMessageDialog(null, "Wrong login or password", "Error", ERROR_MESSAGE);
        });

        // setup sign up button
        signUpButton.addActionListener(e->{
            String login = userField.getText();
            String password = String.valueOf(passwordField.getPassword());

            // Check login
            for(int i=0; i<data.size(); i++) {
                JsonObject userObject = data.getJsonObject(i);
                if(userObject.getString("login").equals(login)) {
                    JOptionPane.showMessageDialog(null, "Login already in use", "Error", ERROR_MESSAGE);
                    return;
                }
            }

            // Check password
            if(password.length() < 5) {
                JOptionPane.showMessageDialog(null, "Password must be longer than 5 characters", "Error", ERROR_MESSAGE);
                return;
            }

            // Add new user to database
            System.out.println(String.format("Adding new user: %s, password: %s", login, password));
        });
    }
}
