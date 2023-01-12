import org.apache.http.NameValuePair;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.message.BasicNameValuePair;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

/**
 * AddBeerWindow is a class that extends JFrame and provides a form for adding new beers.
 * It contains fields for beer name, image, category, and description, as well as buttons for adding the image and submitting the form.
 */
public class AddBeerWindow extends JFrame {
    private JTextField nameField;
    private JButton addImageButton;
    private JComboBox categoryComboBox;
    private JTextArea descriptionArea;
    private JPanel mainPanel;
    private JButton addBeerButton;
    private File imageFile = null;

    /**
     * @param token the user's authentication token
     * @param wnd the MyBeerForm instance, which serves as the main window of the program
     */
    AddBeerWindow(String token, MyBeerForm wnd) {
        setTitle("Add Beer Window");
        add(mainPanel);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        pack();
        setResizable(false);
        setVisible(true);

        String responseString = Backend.getJsonString(Backend.dataURL + "categories", token);
        if(responseString != null) {
            JsonReader reader = Json.createReader(new StringReader(responseString));
            JsonArray array = reader.readArray();
            for(int i=0; i<array.size(); i++) {
                categoryComboBox.addItem(array.getJsonObject(i).getString("name"));
            }
        }

        addImageButton.addActionListener(e->{
            FileNameExtensionFilter filter = new FileNameExtensionFilter(
                    "JPG, PNG, GIF & BMP Images", "jpg", "png", "gif", "bmp", "jpeg", "jfif");

            JFileChooser chooser = new JFileChooser();
            chooser.setFileFilter(filter);

            int returnValue = chooser.showDialog(null, "Add image");
            if(returnValue == JFileChooser.APPROVE_OPTION) {
                imageFile = chooser.getSelectedFile();
                addImageButton.setText(imageFile.getName());
            }
        });

        addBeerButton.addActionListener(e->{
            String name = nameField.getText();
            String description = descriptionArea.getText();

            JsonObject categoryObject = wnd.getCategoriesData().getJsonObject(categoryComboBox.getSelectedIndex());
            int category = categoryObject.getInt("id");

            if(Backend.postBeer(Backend.dataURL + "beers/", name, description, category, imageFile, token) != null) {
                JOptionPane.showMessageDialog(null, "Beer added", "Success", JOptionPane.INFORMATION_MESSAGE);
                wnd.reloadBeers();
                dispose();
            } else {
                JOptionPane.showMessageDialog(null, "Failed to add beer", "Error", ERROR_MESSAGE);
            }
        });
    }
}
