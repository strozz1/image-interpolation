import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QSizePolicy, QSpacerItem, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QPushButton,  QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from dual_image import DualImageViewer
from image_widget import ImageSelectable 
from interp import interpolate,nearest,bilineal, none_interp

class MainImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        #TODO not working
        self.zoom_factor = 1.0
        self.image_path = None
        self.interp_method=nearest
        self.initUI()

       
    def initUI(self):
        self.setWindowTitle('Image interpolation')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout(self)

        #Button layout
        button_layout = QHBoxLayout()
        select_image_button = QPushButton('Open Image')
        select_image_button.clicked.connect(self.open_image)
        button_layout.addWidget(select_image_button) 

        zoom_in_button = QPushButton('Zoom In')
        zoom_in_button.clicked.connect(self.zoom_in)
        #button_layout.addWidget(zoom_in_button)

        select_in_button = QPushButton('Select')
        select_in_button.clicked.connect(self.interp_window)
        button_layout.addWidget(select_in_button)
        type_layout = QHBoxLayout()

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        type_layout.addItem(spacer)

        combobox= QComboBox()
        combobox.addItems(["Nearest neighbor","Bilinear"])
        combobox.currentTextChanged.connect(self.interp_changed)
        type_layout.addWidget(combobox)

        label=QLabel("Type")
        label.setScaledContents(True)      
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        type_layout.addWidget(label)

        button_layout.addLayout(type_layout)
 
        main_layout.addLayout(button_layout)

        # scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        content = QWidget()
        self.scroll_area.setWidget(content)

        #Content layout
        v_layout = QVBoxLayout(content)
        self.image_label = ImageSelectable("")
        v_layout.addWidget(self.image_label,alignment=Qt.AlignCenter)

    def interp_changed(self,method):
        if method == "Bilinear":
            self.interp_method=bilineal
        elif method == "Nearest neighbor":
            method=nearest
    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_image()

    def open_image(self):
        file_dialog = QFileDialog(self)
        image_file, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if image_file:
            self.load_image(image_file)

    def load_image(self, image_path):
        self.image_path = image_path
        self.zoom_factor = 1.0 #todo
        self.update_image()

    def update_image(self):
        self.image_label.setImage(self.image_path)
    
    def interp_window(self):
        method=self.interp_method
        old=self.image_label.data

        self.interpolate(old,method)
       
    def interpolate(self,data,method):
        '''
        Interpolate taking the current selected method, the raw data from label and opens new window with result
        '''
        (x0,y0)=(self.image_label.start_point.x(),self.image_label.start_point.y())
        (x1,y1)=(self.image_label.end_point.x(),self.image_label.end_point.y())

        o_height,o_width=data.shape
        nw,nh=(y1-y0),(x1-x0)

        #The factor needs some rethink... not very good
        factor_h=o_height/nh
        factor_w=o_width/nw
        factor=max(factor_h,factor_w)

        section=data[y0:y1,x0:x1]
        
        new=interpolate(section,factor,method)
        old=interpolate(section,factor,none_interp)
        self.image_window = DualImageViewer(new,old)
        self.image_window.show()
        self.image_label.reset_rect()
        



