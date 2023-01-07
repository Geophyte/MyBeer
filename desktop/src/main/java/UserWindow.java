import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.util.EntityUtils;

import javax.swing.*;
import javax.json.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.*;

public class UserWindow extends JFrame {
    private JPanel mainPanel;
    private JLabel userIcon;
    private JTextPane userData;

    private static final String user_url = "http://127.0.0.1:8000/api/v1/auth/user";

    UserWindow(JsonObject userObject) {
        setTitle("User Window");
        add(mainPanel);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        pack();
        setResizable(false);
        setVisible(true);

        ImageIcon imgIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon("user.png").getImage(), 200, 200));
        userIcon.setIcon(imgIcon);
        userData.setContentType("text/html");
        String html = "<html>username: %s<br>email: %s</html>";
        userData.setText(String.format(html,
                userObject.getJsonObject("user_info").getString("username"),
                userObject.getJsonObject("user_info").getString("email")));
        userData.setEditable(false);

        addWindowFocusListener(new WindowAdapter() {
            @Override
            public void windowDeactivated(WindowEvent e) {
                dispose();
            }
        });
    }
}
