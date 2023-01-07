import org.apache.http.client.methods.HttpGet;

import javax.json.*;
import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import java.awt.*;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.StringReader;

public class MyBeerForm {
    private JTextField searchField;
    private JButton searchButton;
    private JButton filterButton;
    private JComboBox searchCategoryComboBox;
    private JButton userButton;
    private JLabel usernameLabel;
    private JLabel beerImage;
    private JTextPane beerInfoPane;
    private JScrollPane beerPane;
    private DefaultListModel beerListModel;
    private JPanel beerPagePanel;
    private JTree commentTree;
    private JPanel mainPanel;
    private JButton postReviewButton;
    private JComboBox ratingComboBox;
    private JTextField titleFiled;
    private JTextArea reviewArea;
    private JsonObject currUserData;
    private String token;
    private JsonObject currBeer;
    private JsonArray beersData;

    MyBeerForm(String _token) {
        JFrame frame = new JFrame("MyBeer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setIconImage(new ImageIcon("beer20x20.png").getImage());
        frame.setMinimumSize(new Dimension(800, 600));
        frame.add(mainPanel);
        frame.pack();
        frame.setVisible(true);


        token = _token;

        initSearchPanel();
        initUserPanel();
        initBeerPanel();


        loadBeers(Backend.dataURL + "beers");
    }

    private void initSearchPanel() {
        searchField.addFocusListener(new FocusListener() {
            @Override
            public void focusGained(FocusEvent e) {
                if (searchField.getText().equals("Search")) {
                    searchField.setText("");
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (searchField.getText().isEmpty()) {
                    searchField.setText("Search");
                }
            }
        });
        searchField.addActionListener(e->System.out.printf("Searching for %s!%n", searchField.getText()));

        ImageIcon searchIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon("loupe.png").getImage(), 30, 30));
        searchButton.setIcon(searchIcon);
        searchButton.addActionListener(e->{
            System.out.println("Searching");
            String name = "";
            String searchName = searchField.getText();
            if(!searchName.equals("Search") && !searchName.isBlank() && !searchName.isEmpty())
                name = "?name=" + searchField.getText();
            String category = "";
            if(searchCategoryComboBox.isVisible())
            {
                category = "?category=" + (String) searchCategoryComboBox.getItemAt(searchCategoryComboBox.getSelectedIndex());
                if(!name.isEmpty()) name += "&";
            }

            loadBeers(Backend.dataURL + "beers/" + name + category);
        });

        ImageIcon filterIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon("filter.png").getImage(), 30, 30));
        filterButton.setIcon(filterIcon);
        filterButton.addActionListener(e->{
            searchCategoryComboBox.setVisible(!searchCategoryComboBox.isVisible());
            searchCategoryComboBox.setEnabled(!searchCategoryComboBox.isEnabled());
        });

        String responseString = Backend.getJsonString(Backend.dataURL + "categories", token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonArray array = reader.readArray();
            for(int i=0; i<array.size(); i++) {
                searchCategoryComboBox.addItem(array.getJsonObject(i).getString("name"));
            }
        }
    }

    private void initUserPanel() {
        ImageIcon imgIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon("user.png").getImage(), 20, 20));
        userButton.setIcon(imgIcon);

        String responseString = Backend.getJsonString(Backend.userURL, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            currUserData = reader.readObject();

            usernameLabel.setText(currUserData.getJsonObject("user_info").getString("username"));
        }

        userButton.addActionListener(e->{
            UserWindow wnd = new UserWindow(currUserData);
            wnd.setLocationRelativeTo(userButton);
        });
    }

    private void initBeerPanel() {
        // Setup beer list
        beerListModel = new DefaultListModel();
        JList beerList = new JList(beerListModel);
        beerList.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                JList src = (JList) e.getSource();
                if(e.getClickCount() == 2) {
                    int idx = src.locationToIndex(e.getPoint());
                    loadBeerPage(idx);
                }
            }
        });
        beerPane.getViewport().add(beerList);

        // Set up beer page
        beerInfoPane.setEditable(false);

        commentTree = new JTree(new DefaultMutableTreeNode("Reviews"));
        commentTree.setCellRenderer(new CommentTreeCellRenderer());
        commentTree.setCellEditor(new CommentTreeCellEditor(commentTree, (DefaultTreeCellRenderer) commentTree.getCellRenderer()));
        commentTree.setEditable(true);

        beerPagePanel.add(commentTree, BorderLayout.CENTER);

        // Set up review form
        for(int i=1; i<=10; i++) {
            ratingComboBox.addItem(i);
        }

        postReviewButton.addActionListener(e->{
            int beerId = currBeer.getInt("id");
            int rating = ratingComboBox.getSelectedIndex() + 1;
            String title = titleFiled.getText();
            String content = reviewArea.getText();

            String json = "{\"title\": \"" + title + "\"," +
                    "  \"content\": \"" + content +"\"," +
                    "  \"beer\": " + beerId + "," +
                    "  \"rating\":" + rating +" }";
            if(Backend.post(Backend.dataURL + "reviews/", json, token) != null) {
                titleFiled.setText("");
                reviewArea.setText("");
                reloadReviewsAndComments();
            }

        });
    }

    private void loadBeers(String url) {
        // Load data
        String responseString = Backend.getJsonString(url, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            beersData = reader.readArray();
            loadBeerList();
            loadBeerPage(0);
        }
    }

    private void loadBeerList() {
        beerListModel.clear();
        for(int i=0; i<beersData.size(); i++) {
            JsonObject beerObject = beersData.getJsonObject(i);
            String name = beerObject.getString("name");
            beerListModel.addElement(name);
        }
    }

    private void loadBeerPage(int idx) {
        JsonObject beerObject = beersData.getJsonObject(idx);

        // display image
        BufferedImage image = Backend.getImage(beerObject.getString("image_url"));
        if(image != null) {

            beerImage.setIcon(new ImageIcon(Utility.getScaledImage(image, 200, 200)));
        }
        else {
            ImageIcon beerIcon = new ImageIcon(Utility.getScaledImage(new ImageIcon("beer.png").getImage(), 200, 200));
            beerImage.setIcon(beerIcon);
        }

        String name = beerObject.getString("name");
        String description = beerObject.getString("description").replaceAll("\n", "<br>");

        String rating = "";
        JsonValue ratingValue = beerObject.get("rating");
        if(ratingValue != null && ratingValue.getValueType() == JsonValue.ValueType.NUMBER) {
            rating = String.valueOf(beerObject.getJsonNumber("rating").doubleValue());
        } else {
            rating = "-";
        }

        String html = "<html><body style='width: %1spx'>" +
                "<h1>" + name + "</h1>" +
                "<p>%s</p>" +
                "<p>Ocena: " + rating + " / 10 <p>" +
                "</html>";
        beerInfoPane.setContentType("text/html");
        beerInfoPane.setText(String.format(html, 300, description));

        currBeer = beerObject;
        loadReviewsAndComments(currBeer);

        titleFiled.setText("");
        reviewArea.setText("");
    }

    private void loadReviewsAndComments(JsonObject beerObject) {
        DefaultTreeModel model = (DefaultTreeModel) commentTree.getModel();
        DefaultMutableTreeNode root = (DefaultMutableTreeNode) model.getRoot();
        root.removeAllChildren();
        model.reload();

        // load reviews
        String responseString = Backend.getJsonString(Backend.dataURL + "reviews/?beer_id=" + beerObject.getInt("id"), token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonArray reviewArray = reader.readArray();

            for(int i=0; i<reviewArray.size(); i++) {
                JsonObject reviewObject = reviewArray.getJsonObject(i);
                DefaultMutableTreeNode newRoot = new DefaultMutableTreeNode(new ReviewForm(token, reviewObject, this));

                root.add(newRoot);

                responseString = Backend.getJsonString(Backend.dataURL + "/comments/?review=" + reviewObject.getInt("id"), token);
                if(responseString != null) {
                    reader = Json.createReader(new StringReader(responseString));
                    JsonArray commentArray = reader.readArray();

                    for(int j=0; j<commentArray.size(); j++) {
                        JsonObject commentObject = commentArray.getJsonObject(j);
                        DefaultMutableTreeNode newComment = new DefaultMutableTreeNode(new CommentForm(token, commentObject));

                        newRoot.add(newComment);
                    }
                }
            }
        }

        beerPagePanel.revalidate();
        commentTree.expandRow(0);
    }

    public void reloadReviewsAndComments() {
        loadReviewsAndComments(currBeer);
    }
}

