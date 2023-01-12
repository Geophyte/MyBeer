import javax.swing.*;
import javax.swing.tree.DefaultTreeCellEditor;
import javax.swing.tree.DefaultTreeCellRenderer;
import java.awt.*;
import java.util.EventObject;

/**
 * CommentTreeCellEditor is a class that extends DefaultTreeCellEditor.
 * It is used to provide custom behavior for editing cells in a JTree component.
 */
public class CommentTreeCellEditor extends DefaultTreeCellEditor {
    public CommentTreeCellEditor(JTree tree, DefaultTreeCellRenderer renderer) {
        super(tree, renderer);
    }
    public Component getTreeCellEditorComponent (JTree tree, Object value, boolean isSelected, boolean expanded, boolean leaf, int row )
    {
        return renderer.getTreeCellRendererComponent(tree, value, true, expanded, leaf, row, true);
    }
    public boolean isCellEditable ( EventObject anEvent )
    {
        return true;
    }
}
