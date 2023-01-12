import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreePath;
import java.awt.*;
import java.io.StringReader;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

/**
 * The ReviewForm class is responsible for displaying the details of a review in a user-friendly manner. It allows users to view the details of the review, such as the author, rating, title, and content, as well as the ability to add comments to the review.
 * The class takes in a token, a reviewObject representing the review, and a wnd object of type MyBeerForm as arguments.
 * It first loads the author data by fetching the author's information using the provided token, and displaying the author's username as a button. Clicking on the button opens a new UserWindow with the author's information.
 * It then sets the rating and title of the review, and formats the content of the review by replacing all newline characters with <br>.
 * The class also includes functionality to add comments to the review by sending a post request to the server with the comment's content and the review's id, and displaying a message indicating whether the comment was added successfully or not.
 * It also includes a button to toggle the visibility of comments on the review, and a border around the main panel.
 */
public class ReviewForm {
    private JButton authorButton;
    private JLabel ratingLabel;
    private JTextPane reviewPane;
    private JButton addCommentButton;
    private JTextArea commentArea;
    private JPanel mainPanel;
    private JLabel titleLabel;
    private JButton commentsButton;
    private boolean showComments = true;

    ReviewForm(String token, JsonObject reviewObject, MyBeerForm wnd) {
        // load author data
        int authorID = reviewObject.getInt("author");

        String responseString = Backend.getJsonString(Backend.dataURL + "users/" + authorID, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonObject userObject = reader.readObject();

            String author = userObject.getString("username");

            authorButton.setText(author);
            authorButton.addActionListener(e-> {
                new UserWindow(userObject).setLocationRelativeTo(authorButton);
            });
        } else {
            authorButton.setText("[Unknown]");
        }

        int rating = reviewObject.getInt("rating");
        ratingLabel.setText(rating + " / 10");

        String title = reviewObject.getString("title");
        titleLabel.setText(title);

        String content = reviewObject.getString("content").replaceAll("\n", "<br>");
        String html = "<html><body style='width: %1spx'>" +
                "%s" +
                "</html>";

        reviewPane.setContentType("text/html");
        reviewPane.setText(String.format(html, 300, content));

        addCommentButton.addActionListener(e->{
            String json = "{" +
                    "\"content\": " + "\"" + commentArea.getText() + "\"," +
                    "\"review\": " + reviewObject.getInt("id") +
                    "}";
            System.out.println(json);

            if(Backend.post(Backend.dataURL + "comments/", json, token) == null) {
                JOptionPane.showMessageDialog(null, "Failed to add comment", "Error", ERROR_MESSAGE);
            }

            commentArea.setText("");
            wnd.reloadReviewsAndComments();
        });


        commentsButton.addActionListener(e->{
            if(showComments) {
                commentsButton.setText("Hide comments");
                DefaultMutableTreeNode node = (DefaultMutableTreeNode) wnd.getCommentTree().getLastSelectedPathComponent();
                if(!node.isLeaf())
                    wnd.getCommentTree().expandPath(new TreePath(node.getPath()));
            } else {
                commentsButton.setText("Show comments");
                DefaultMutableTreeNode node = (DefaultMutableTreeNode) wnd.getCommentTree().getLastSelectedPathComponent();
                if(!node.isLeaf())
                    wnd.getCommentTree().collapsePath(new TreePath(node.getPath()));
            }

            showComments = !showComments;
        });

        Border border = new LineBorder(Color.lightGray, 1);
        mainPanel.setBorder(border);
    }

    public JPanel getMainPanel() {
        return mainPanel;
    }
}
