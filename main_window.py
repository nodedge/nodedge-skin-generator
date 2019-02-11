import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):

    stylesheet_filename = "qss/skin.qss"
    stylesheet_last_modified = 0

    def __init__(self):
        super().__init__()

        self.organization = 'Blenderfreak'
        self.application = 'QSS Style Tester'

        self.load_default_skin()

        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(500.0)
        self.timer.timeout.connect(self.check_stylesheet)
        self.timer.start()

        self.readSettings()

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage("Ready")
        self.initActions()
        self.initMenus()
        self.setWindowTitle("BlenderFreak's QSS Style Tester")

    def initMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

    def initActions(self):
        self.actNew = QAction("&New", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)
        self.actOpen = QAction("&Open", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)
        self.actSave = QAction("&Save", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)
        self.actSaveAs = QAction("Save &As", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)
        self.actExit = QAction("E&xit", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)

        self.actUndo = QAction("&Undo", self, shortcut='Ctrl+Z', statusTip="Undo", triggered=self.noop)
        self.actRedo = QAction("&Redo", self, shortcut='Ctrl+Y', statusTip="Redo", triggered=self.noop)
        self.actCut = QAction("C&ut", self, shortcut='Ctrl+X', statusTip="Redo", triggered=self.noop)
        self.actCopy = QAction("&Copy", self, shortcut='Ctrl+C', statusTip="Copy", triggered=self.noop)
        self.actPaste = QAction("&Paste", self, shortcut='Ctrl+V', statusTip="Paste", triggered=self.noop)
        self.actDelete = QAction("&Delete", self, shortcut='Del', statusTip="Redo", triggered=self.noop)

        self.actAbout = QAction("&About", self, statusTip="About this app", triggered=self.about)

    def noop(self):
        pass

    def about(self):
        QMessageBox.about(self, "About", "This is just a testing application with live reload of QSS Skin")

    def readSettings(self):
        settings = QSettings(self.organization, self.application)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.organization, self.application)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def load_default_skin(self, num_style_key=2):
        if num_style_key is None: return        # ignore setting default style when passed None
        QApplication.setStyle(QStyleFactory.create(QStyleFactory.keys()[num_style_key]))
        print("QStyleFactory keys:", QStyleFactory.keys())
        print("Set:", QStyleFactory.keys()[num_style_key])

    def check_stylesheet(self, filename=None):
        if filename is None: filename = self.__class__.stylesheet_filename
        try:
            mod_time = os.path.getmtime(filename)
        except FileNotFoundError:
            print('stylesheet "%s" was not found' % filename)
            return

        if mod_time != MainWindow.stylesheet_last_modified:
            MainWindow.stylesheet_last_modified = mod_time
            self.reload_stylesheet(filename)

    def reload_stylesheet(self, filename=None):
        if filename is None: filename = self.__class__.stylesheet_filename
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = str(file.readAll(), encoding='utf-8')
        print("reloading: %s" % filename)
        QApplication.instance().setStyleSheet(stylesheet)

