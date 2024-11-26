import sys

from PyQt5.QtWidgets import QApplication
from gui import MainImageViewer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MainImageViewer()
    viewer.show()
    sys.exit(app.exec_())
