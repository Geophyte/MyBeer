import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellEditor;
import javax.swing.tree.DefaultTreeCellRenderer;
import java.awt.*;

/**
 * CommentTreeCellRenderer is a class that extends DefaultTreeCellRenderer.
 * It is used to provide custom behavior for rendering cells in a JTree component.
 */
public class CommentTreeCellRenderer extends DefaultTreeCellRenderer {
    @Override
    public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
        super.getTreeCellRendererComponent(tree, value, selected, expanded, leaf, row, hasFocus);
        DefaultMutableTreeNode node = (DefaultMutableTreeNode) value;
        Object userObject = node.getUserObject();
        if(userObject instanceof CommentForm) {
            return ((CommentForm) userObject).getMainPanel();
        } else if (userObject instanceof  ReviewForm) {
            return ((ReviewForm) userObject).getMainPanel();
        } else {
            String text = (String) userObject;
            JTextPane defaultPane = new JTextPane();
            defaultPane.setText(text);
            return defaultPane;
        }
    }
}

