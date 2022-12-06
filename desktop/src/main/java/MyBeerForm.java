import javax.json.JsonReader;
import javax.swing.*;
import java.awt.*;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import javax.json.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;

public class MyBeerForm {
    private JTextField searchField;
    private JButton searchButton;
    private JButton filterButton;
    private JButton userButton;
    private JLabel userName;
    private JTextPane beerInfo;
    private JPanel mainPanel;
    private JLabel beerImage;
    private JScrollPane beerPane;
    private JPanel reviewPanel;
    private DefaultListModel beerListModel;
    private JTree commentTree;
    private JButton addCommentButton;
    private JsonArray data;

    MyBeerForm() throws FileNotFoundException {
        // read JSON file
        InputStream fis = new FileInputStream("beers.json");
        JsonReader reader = Json.createReader(fis);
        data = reader.readArray();
        reader.close();

        // =========================== SEARCH BAR ===========================
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

        ImageIcon searchIcon = new ImageIcon(getScaledImage(new ImageIcon("loupe.png").getImage(), 30, 30));
        searchButton.addActionListener(e->System.out.printf("Searching for %s!%n", searchField.getText()));
        searchButton.setIcon(searchIcon);

        ImageIcon filterIcon = new ImageIcon(getScaledImage(new ImageIcon("filter.png").getImage(), 30, 30));
        filterButton.addActionListener(e->System.out.println("Opening filter window"));
        filterButton.setIcon(filterIcon);
        // ==================================================================

        // =========================== USER SPACE ===========================
        ImageIcon userIcon = new ImageIcon(getScaledImage(new ImageIcon("user.png").getImage(), 30, 30));
        userButton.addActionListener(e->System.out.println("Displaying user data"));
        userButton.setIcon(userIcon);
        // ==================================================================

        // =========================== BEER PAGE ============================
        ImageIcon beerIcon = new ImageIcon(getScaledImage(new ImageIcon("beer.png").getImage(), 200, 200));
        beerImage.setIcon(beerIcon);

        beerListModel = new DefaultListModel();
        JList beerList = new JList(beerListModel);
        beerList.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                JList src = (JList) e.getSource();
                if(e.getClickCount() == 2) {
                    int idx = src.locationToIndex(e.getPoint());
                    loadBeerPage(idx, data);
                }
            }
        });
        beerPane.getViewport().add(beerList);

        commentTree = new JTree(new DefaultMutableTreeNode("Comments"));
        reviewPanel.add(commentTree, BorderLayout.SOUTH);
        // ==================================================================

        // Add components
        JFrame wndFrame = new JFrame();
        wndFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        wndFrame.setIconImage(new ImageIcon("beer.png").getImage());
        wndFrame.setVisible(true);
        wndFrame.setMinimumSize(new Dimension(600, 400));
        wndFrame.add(mainPanel);

        // load beer list (list on left side)
        for(int i=0; i<data.size(); i++) {
            JsonObject beerObject = data.getJsonObject(i);
            beerListModel.addElement(beerObject.getString("name"));
        }

        // load first beer page
        loadBeerPage(0, data);
    }

    private Image getScaledImage(Image srcImg, int w, int h){
        BufferedImage resizedImg = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = resizedImg.createGraphics();

        g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2.drawImage(srcImg, 0, 0, w, h, null);
        g2.dispose();

        return resizedImg;
    }

    public void loadBeerPage(int idx, JsonArray data) {
        JsonObject beerObject = data.getJsonObject(idx);
        System.out.printf("Loading page %d%n", idx);

        // set photo
        ImageIcon beerIcon = new ImageIcon(getScaledImage(new ImageIcon(beerObject.getString("photo")).getImage(), 200, 200));
        beerImage.setIcon(beerIcon);

        // set description
        beerInfo.setContentType(beerObject.getString("description_type"));
        beerInfo.setText(beerObject.getString("description"));

        // set comments
        DefaultTreeModel model = (DefaultTreeModel) commentTree.getModel();
        DefaultMutableTreeNode root = (DefaultMutableTreeNode) model.getRoot();
        root.removeAllChildren();
        model.reload();
        JsonArray comments = beerObject.getJsonArray("comments");
        for(int i=0; i<comments.size(); i++) {
            root.add(loadComments(comments.getJsonObject(i)));
        }
        reviewPanel.revalidate();

        // expand comment tree
        for(int i=0; i<commentTree.getRowCount(); i++) {
            commentTree.expandRow(i);
        }
    }

    private DefaultMutableTreeNode loadComments(JsonObject jsonRoot) {
        String comment = String.format("%s: %s", jsonRoot.getString("user"), jsonRoot.getString("comment"));
        String html = "<html><body style='width: %1spx'>%1s";
        DefaultMutableTreeNode newRoot = new DefaultMutableTreeNode(String.format(html, 200, comment));

        JsonArray replies = jsonRoot.getJsonArray("replies");
        for(int i=0; i<replies.size(); i++) {
            newRoot.add(loadComments(replies.getJsonObject(i)));
        }

        return newRoot;
    }
}