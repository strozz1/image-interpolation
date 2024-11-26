import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect,QPoint

__all__=['ImageSelectable','Numpy_to_qpixmap','scale_pixmap']


#Thanks chatgpt
def scale_pixmap(pixmap, width, height, keep_aspect_ratio=True):
    transform_mode = Qt.FastTransformation
    if keep_aspect_ratio:
        return pixmap.scaled(width, height, Qt.KeepAspectRatio, transform_mode)
    else:
        return pixmap.scaled(width, height, Qt.IgnoreAspectRatio, transform_mode)

def qpixmap_to_grayscale_numpy(pixmap):
    # Convert QPixmap to QImage
    q_image = pixmap.toImage()

    # Ensure the QImage is in Format_Grayscale8
    q_image = q_image.convertToFormat(QImage.Format_Grayscale8)

    # Extract image dimensions
    width = q_image.width()
    height = q_image.height()

    # Extract pixel data as a NumPy array
    ptr = q_image.bits()
    ptr.setsize(height * width)  # Set size of raw data
    gray_array = np.array(ptr).reshape((height, width))

    return gray_array
def Numpy_to_qpixmap(np_array):
    # Ensure the array is in uint8 format (0-255 grayscale values)
    if np_array.dtype != np.uint8:
        raise ValueError("The NumPy array must be of type uint8 for QImage.")
    np_array = np.ascontiguousarray(np_array)
    # Get dimensions
    shape = np_array.shape

    # Create a QImage from the NumPy array
    if len(shape) == 2 or (len(shape) == 3 and shape[2] == 1):
        height, width = shape[:2]
        q_image = QImage(np_array.data, width, height, QImage.Format_Grayscale8)

    # RGB image (3 channels)
    elif len(shape) == 3 and shape[2] == 3:
        height, width, _ = shape
        q_image = QImage(np_array.data, width, height, 3 * width, QImage.Format_RGB888)

    else:
        raise ValueError("Unsupported NumPy array shape. Expected (H, W) or (H, W, 3).")
    # Convert QImage to QPixmap
    pixmap = QPixmap.fromImage(q_image)
    return pixmap


class ImageSelectable(QWidget):
    '''
    Image widget with selection behaviour.
    Contains the raw image in the 'data' attribute, which is then used in 'image' pixmap.
    '''
    def __init__(self, image_path):
        super().__init__()
        self.setImage(image_path)
        
    def setImage(self,path):
        pixmap=QPixmap(path)
        self.image=pixmap
        #make grayscale
        if not pixmap.isNull():
            # Convert to gray scale
            self.data=qpixmap_to_grayscale_numpy(pixmap)
            self.image=Numpy_to_qpixmap(self.data)
        self.start_point = None
        self.end_point = None
        self.rect = None
        self.setFixedSize(self.image.size())


    def mousePressEvent(self, event):
        # Check if the click is within the image area
        if event.pos().x() < self.image.width() and event.pos().y() < self.image.height():
            self.start_point = event.pos()
            self.rect = None  # Reset rectangle

    def mouseMoveEvent(self, event):
        if self.start_point:
            # Limit the end point to the image bounds
            x = min(event.pos().x(), self.image.width() - 1)
            y = min(event.pos().y(), self.image.height() - 1)
            self.end_point = QPoint(x, y)
            self.rect = QRect(self.start_point, self.end_point)
            print(self.rect)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.start_point:
            # Limit the end point to the image bounds
            x = min(event.pos().x(), self.image.width() - 1)
            y = min(event.pos().y(), self.image.height() - 1)
            self.end_point = QPoint(x, y)
            #self.rect = QRect(self.start_point, self.end_point)
            self.update()
    def reset_rect(self):
        self.start_point= None
        self.end_point= None
        self.rect= None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the image
        painter.drawPixmap(0, 0, self.image)

        # Draw the rectangle if it exists
        if self.rect:
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.rect)


