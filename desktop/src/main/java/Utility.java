import java.awt.*;
import java.awt.image.BufferedImage;

/**
 * The Utility class contains a single static method for scaling images.
 */
public class Utility {
    /**
     * @param srcImg : the original image to be scaled
     * @param w : the width of the scaled image
     * @param h : the height of the scaled image
     * @return : the scaled image
     */
    public static Image getScaledImage(Image srcImg, int w, int h) {
        BufferedImage resizedImg = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = resizedImg.createGraphics();

        g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2.drawImage(srcImg, 0, 0, w, h, null);
        g2.dispose();

        return resizedImg;
    }
}
