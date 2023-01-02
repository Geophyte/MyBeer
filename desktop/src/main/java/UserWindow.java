import netscape.javascript.JSObject;

import javax.swing.*;
import javax.json.*;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

public class UserWindow {
    private JPanel mainPanel;
    private JLabel userIcon;
    private JTextPane userData;
    private JsonArray data;

    UserWindow(String userLogin) throws FileNotFoundException {
        // Load users data
        InputStream fis = new FileInputStream("users.json");
        JsonReader reader = Json.createReader(fis);
        data = reader.readArray();
        reader.close();

        loadUser(userLogin);
    }

    void loadUser(String userLogin){
        // Find right user
        for(int i=0; i<data.size(); i++) {
            JsonObject userObject = data.getJsonObject(i);
            if(userObject.getString("login").equals(userLogin)) {
                ImageIcon imgIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon(userObject.getString("image")).getImage(), 200, 200));
                userIcon.setIcon(imgIcon);
                userData.setContentType("text/html");
                userData.setText(String.format("<html>login: %s, password: %s</html>", userObject.getString("login"), userObject.getString("password")));

                JFrame frame = new JFrame("User Info");
                frame.add(mainPanel);
                frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                frame.pack();
                frame.setResizable(false);
                frame.setVisible(true);
            }
        }
    }
}
