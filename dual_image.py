from PyQt5.QtWidgets import  QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,  QLabel, QScrollArea
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QSize, Qt

from image_widget import Numpy_to_qpixmap, scale_pixmap

__all__=['DualImageViewer']

class ImageViewer(QScrollArea):
    def __init__(self,img):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.setWidget(self.content)
        self.image_label = QLabel(self.content)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout(self.content)
        self.layout.addWidget(self.image_label)
        self.set_image(img)

    def set_image(self,img):
        pixmap = Numpy_to_qpixmap(img)
        self.image_label.setPixmap(pixmap)

       
class DualImageViewer(QMainWindow):
    def __init__(self,new,old, parent=None):
        super().__init__(parent)
        self.initUI(new,old)

    def initUI(self,new,old):
        self.setWindowTitle('Interpolation result')
        self.setGeometry(100, 100, 1200, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create image layout
        image_layout = QHBoxLayout()

        self.left_viewer = ImageViewer(old)
        image_layout.addWidget(self.left_viewer)
      
        
        self.right_viewer = ImageViewer(new)
        image_layout.addWidget(self.right_viewer)

        main_layout.addLayout(image_layout)


