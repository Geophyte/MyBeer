import org.apache.http.client.utils.URIBuilder;

import javax.json.*;
import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.StringReader;
import java.net.URISyntaxException;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

/**
 * Main application window that is created right after user logs in
 * It provides options for user to add reviews, comment, and add new beers
 * as well as search for beers by name and/or category
 */
public class MyBeerForm extends JFrame {
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
    private JButton logOutButton;
    private JButton addBeerButton;
    private JsonObject currUserData;
    private JsonArray beersData;
    private JsonArray categoriesData;
    private String token;
    private JsonObject currBeer;

    MyBeerForm(String _token) {
        setTitle("MyBeer");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setIconImage(new ImageIcon("beer20x20.png").getImage());
        setMinimumSize(new Dimension(800, 600));
        add(mainPanel);
        pack();
        setVisible(true);

        token = _token;

        initSearchPanel();
        initUserPanel();
        initBeerPanel();


        loadBeers(Backend.dataURL + "beers");
    }

    /**
     * Initialize search panel, that is:
     * search field, setting it up typically for a search bar
     * search button, filter button and category drop down list
     */
    private void initSearchPanel() {
        final ActionListener searchListener = e->{
            try {
                URIBuilder builder = new URIBuilder(Backend.dataURL + "beers/");

                String searchName = searchField.getText();
                if(!searchName.equals("Search") && !searchName.isBlank() && !searchName.isEmpty())
                    builder.addParameter("name", searchName);
                if(searchCategoryComboBox.isVisible())
                    builder.addParameter("category", (String) searchCategoryComboBox.getItemAt(searchCategoryComboBox.getSelectedIndex()));

                loadBeers(String.valueOf(builder.build()));
            } catch (URISyntaxException ex) {
                throw new RuntimeException(ex);
            }
        };

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
        searchField.addActionListener(searchListener);

        ImageIcon searchIcon = new ImageIcon("search.png");
        searchButton.setIcon(searchIcon);
        searchButton.addActionListener(searchListener);

        ImageIcon filterIcon = new ImageIcon("filter20x20.png");
        filterButton.setIcon(filterIcon);
        filterButton.addActionListener(e->{
            searchCategoryComboBox.setVisible(!searchCategoryComboBox.isVisible());
            searchCategoryComboBox.setEnabled(!searchCategoryComboBox.isEnabled());
        });

        String responseString = Backend.getJsonString(Backend.dataURL + "categories", token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            categoriesData = reader.readArray();
            for(int i=0; i<categoriesData.size(); i++) {
                searchCategoryComboBox.addItem(categoriesData.getJsonObject(i).getString("name"));
            }
        }
    }

    /**
     * Initialize user panel:
     * user button, username and logout button
     */
    private void initUserPanel() {
        ImageIcon imgIcon = new ImageIcon("user20x20.png");
        userButton.setIcon(imgIcon);

        String responseString = Backend.getJsonString(Backend.userURL, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            currUserData = reader.readObject().getJsonObject("user_info");

            usernameLabel.setText(currUserData.getString("username"));
        }

        userButton.addActionListener(e->{
            UserWindow wnd = new UserWindow(currUserData);
            wnd.setLocationRelativeTo(userButton);
        });

        logOutButton.addActionListener(e->{
            Backend.post(Backend.logoutURL, token);
            new LoginWindow();
            setDefaultCloseOperation(DISPOSE_ON_CLOSE);
            dispose();
        });
    }

    /**
     * Initialize beer panel:
     * beer list, beer button, comment tree
     * and add review form
     */
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

        addBeerButton.addActionListener(e->{
            new AddBeerWindow(token, this);
        });

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

            if(title.isEmpty() || title.isBlank())
            {
                JOptionPane.showMessageDialog(null, "Review needs non empty title", "Error", ERROR_MESSAGE);
                return;
            }
            if(content.isEmpty() || content.isBlank()) {
                JOptionPane.showMessageDialog(null, "Review needs non empty content", "Error", ERROR_MESSAGE);
                return;
            }

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

    /**
     * Load beers from url. Beers are loaded into BeerData JsonArray
     * after that all beer names are loaded into beer list.
     * The first beer page in a list is loaded (if no beers are present in beer list
     * an error message is displayed)
     * @param url url to beer data
     */
    private void loadBeers(String url) {
        // Load data
        String responseString = Backend.getJsonString(url, token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            beersData = reader.readArray();
            loadBeerList();
            if(beersData.size() > 0)
                loadBeerPage(0);
            else
                JOptionPane.showMessageDialog(null, "No beers found", "Error", ERROR_MESSAGE);
        }
    }

    /**
     * Populates beer list with beer names
     */
    private void loadBeerList() {
        beerListModel.clear();
        for(int i=0; i<beersData.size(); i++) {
            JsonObject beerObject = beersData.getJsonObject(i);
            String name = beerObject.getString("name");
            beerListModel.addElement(name);
        }
    }

    /**
     * Loads beer page for a beer
     * @param idx id of a beer to be loaded
     */
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

        String rating = "-";
        JsonValue ratingValue = beerObject.get("rating");
        if(!ratingValue.toString().equals("null")) {
            rating = beerObject.getString("rating");
        }

        String category = beerObject.getJsonObject("category").getString("name");

        String html = "<html><body style='width: %1spx'>" +
                "<h1>" + name + "</h1>" +
                "<strong><p>Kategoria: " + category + "</p>" +
                "<p>Ocena: " + rating + " / 10 </p></strong>" +
                "<p>%s</p>" +
                "</html>";
        beerInfoPane.setContentType("text/html");
        beerInfoPane.setText(String.format(html, 300, description));

        currBeer = beerObject;
        loadReviewsAndComments(currBeer);

        titleFiled.setText("");
        reviewArea.setText("");
    }

    /**
     * loads reviews and comment left under a beer
     * @param beerObject JsonObject containing specific beer information
     */
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

    /**
     * Reloads reviews and comments after change on backend
     * for example after adding comment/review
     */
    public void reloadReviewsAndComments() {
        loadReviewsAndComments(currBeer);
    }

    /**
     * Reloads beers after adding in new beer
     */
    public void reloadBeers() {
        loadBeers(Backend.dataURL + "/beers");
    }

    public JsonArray getCategoriesData() {
        return categoriesData;
    }

    public JTree getCommentTree() {
        return commentTree;
    }
}

