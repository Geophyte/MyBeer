import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.io.FileNotFoundException;

public class CommentForm {
    public JPanel mainPanel;
    private JButton authorButton;
    private JTextPane authorDatePane;
    private JTextPane commentPane;

    public CommentForm(String author, String date, ImageIcon authorsPic, String comment) {
        authorButton.setIcon(authorsPic);
        authorButton.addActionListener(e->{
            System.out.println("Comment author clicked");
            try {
                new UserWindow(author);
            } catch (FileNotFoundException ex) {
                throw new RuntimeException(ex);
            }
        });

        String authorDate = String.format(
                "<div class=\"comment\">\n" +
                        "  <div class=\"comment-header\">\n" +
                        "    <span class=\"comment-author\">%s</span>\n" +
                        "    <br>\n" +
                        "    <font size=\"2\"\n" +
                        "    <span class=\"comment-date\">%s</span>\n" +
                        "    </font>\n" +
                        "  </div>\n" +
                        "</div>",
                author, date
        );
        authorDatePane.setContentType("text/html");
        authorDatePane.setText(authorDate);

        commentPane.setContentType("text/html");
        commentPane.setText(comment);

        Border border = new LineBorder(Color.lightGray, 1);
        mainPanel.setBorder(border);
    }
}
