import os
import sys
from PyQt5.QtWidgets import *
from test_window import TestWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = TestWindow()
    # wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec_())
