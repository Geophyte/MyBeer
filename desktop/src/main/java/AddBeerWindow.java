import javax.swing.*;
import java.awt.*;

public class AddBeerWindow extends JFrame {
    private JTextField nameField;
    private JComboBox categoryComboBox;
    private JFileChooser imageFileChooser;
    private JTextArea descriptionArea;
    private JPanel mainPanel;

    AddBeerWindow(String token) {
        imageFileChooser = new JFileChooser();

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 1;
        gbc.gridy = 2;
        mainPanel.add(imageFileChooser, gbc);

        setTitle("Add Beer Window");
        add(mainPanel);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        pack();
        setResizable(false);
        setVisible(true);
    }
}
