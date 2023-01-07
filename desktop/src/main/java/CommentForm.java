import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.io.StringReader;

public class CommentForm {
    private JPanel mainPanel;
    private JButton authorButton;
    private JTextPane commentPane;

    public CommentForm(String token, JsonObject commentData) {
        // load author data
        int authorID = commentData.getInt("author");

        String responseString = Backend.getJsonString(Backend.dataURL + "users/" + authorID, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonObject userObject = reader.readObject();

            String author = userObject.getString("username");

            authorButton.setText(author);
            authorButton.addActionListener(e-> {
                UserWindow wnd = new UserWindow(userObject);
                wnd.setLocationRelativeTo(authorButton);
            });
        } else {
            authorButton.setText("[Unknown]");
        }

        String content = commentData.getString("content").replaceAll("\n", "<br>");
        String html = "<html><body style='width: %1spx'>" +
                "<p>%s</p>" +
                "</html>";

        commentPane.setContentType("text/html");
        commentPane.setText(String.format(html, 300, content));

        Border border = new LineBorder(Color.lightGray, 1);
        mainPanel.setBorder(border);
    }

    public JPanel getMainPanel() {
        return mainPanel;
    }
}
