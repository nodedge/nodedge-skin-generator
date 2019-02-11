import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main_window import MainWindow


class TestWindow(MainWindow):
    instance = None

    def initUI(self):
        # storing refernece to this window, for skins reloading
        self.__class__.instance = self

        super().initUI()

        self.initDocks()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        child = MainContent()
        self.mdiArea.addSubWindow(QTextEdit())
        self.mdiArea.addSubWindow(QTextEdit())
        self.mdiArea.addSubWindow(QTextEdit())
        swnd = self.mdiArea.addSubWindow(child)
        swnd.setWindowTitle("Demo Widgets")



    def initDocks(self):
        dock = QDockWidget("Files", self)
        dock.setWidget(self.createFilesDock())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        dock3 = QDockWidget("Foo", self)
        dock3.setWidget(QTextEdit())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock3)

        dock2 = QDockWidget("Files2", self)
        dock2.setWidget(self.createFilesDock())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock2)
        self.tabifyDockWidget(dock2, dock)

    def createFilesDock(self):
        wdg = QWidget()
        lay = QVBoxLayout(wdg)
        lay.setContentsMargins(QMargins(0, 0, 0, 0))

        lw = QListWidget()
        lw.setAlternatingRowColors(True)
        lay.addWidget(lw)
        for i in range(7): lw.addItem(QListWidgetItem("Item %d" % i))

        tw = QTreeWidget()
        tw.setHeaderItem(QTreeWidgetItem(["Name", "Options"]))
        lay.addWidget(tw)
        tw.setAlternatingRowColors(True)

        root = QTreeWidgetItem(tw, ["Tree Items", "our items"])
        root.setData(2, Qt.EditRole, 'Some hidden data here')
        for i in range(4):
            itm = QTreeWidgetItem(root, ["Item %d" % i, ""])
            itm.setData(2, Qt.EditRole, 'Some hidden data here')

        for i in range(3):
            dir = QTreeWidgetItem(tw, ["Dir%d" % i, ""])
            for j in range(2 - i):
                sd = QTreeWidgetItem(dir, ["SubDir%d" % j, ""])
                for k in range(3): QTreeWidgetItem(sd, ["SubItem %d" % (k + 1)])

        return wdg



class MainContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.createBasicLayout()
        self.createBottomContent()
        self.createLeftContent()
        self.createRightContent()

    def createComboBoxWithQSSStyleSheets(self):
        self.skinCombo = QComboBox()
        self.refreshSkinCombo()
        # self.skinCombo.setCurrentText(TestWindow.stylesheet_filename)

        self.skinCombo.currentTextChanged.connect(self.onSkinChanged)
        return self.skinCombo

    def refreshSkinCombo(self):
        last_text = self.skinCombo.currentText()
        if last_text == "": last_text = TestWindow.stylesheet_filename
        print("last skin:", last_text)

        for i in range(len(self.skinCombo)): self.skinCombo.removeItem(0)

        for dirname, subdirs, filelist in os.walk(os.path.join(os.path.dirname(__file__), 'qss')):
            for fname in filelist:
                name = os.path.join("qss", fname)
                self.skinCombo.addItem(name)

        print("Refreshed Skin Combo from qss/ directory...")

        # in app we use /, this work for linux and even my woe, but it's woe... again
        # we need to do some hacking -.-
        last_text = last_text.replace('/', os.path.sep)

        print("setting skin to:", last_text)
        self.skinCombo.setCurrentText(last_text)

    def onSkinChanged(self, name):
        print("Skin change to:", name)
        TestWindow.stylesheet_filename = os.path.join(os.path.dirname(__file__), name)
        TestWindow.instance.reload_stylesheet()

    def createBottomContent(self):
        lay = QHBoxLayout(self.bottom)

        lay.addWidget(QLabel("Select active QSS Skin"))

        lay.addWidget(self.createComboBoxWithQSSStyleSheets())

        lay.addWidget(QLabel(""))
        qpb = QPushButton("Reload QSS Skins List")
        qpb.clicked.connect(self.refreshSkinCombo)
        lay.addWidget(qpb)

        lay.addStretch()

    def createLeftContent(self):
        main_layout = QHBoxLayout(self.topleft)

        # left part
        wdg_left = QWidget()
        lay = QVBoxLayout(wdg_left)
        main_layout.addWidget(wdg_left)

        ql = QLabel("Simple QLabel")
        ql.setObjectName("Example")
        lay.addWidget(ql)
        lay.addWidget(QLineEdit())
        lay.addWidget(QSpinBox())
        lay.addWidget(QPushButton("QPushButton"))
        qpb = QPushButton("QPushButton#danger")
        qpb.setObjectName("danger")
        lay.addWidget(qpb)
        lay.addWidget(QCheckBox("QCheckBox"))
        lay.addWidget(QCheckBox("QCheckBox2"))
        lay.addWidget(QCheckBox("QCheckBox3"))
        lay.addWidget(QRadioButton("QRadioButton1"))
        lay.addWidget(QRadioButton("QRadioButton2"))
        lay.addWidget(QRadioButton("QRadioButton3"))

        combo_box = QComboBox()
        combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        lay.addWidget(combo_box)
        qtex = QTextEdit("Some TextEdit text for editing...")
        qtex.setMaximumHeight(50)
        lay.addWidget(qtex)


        lay.addStretch()

        # right part
        wdg_right = QWidget()
        lay = QHBoxLayout(wdg_right)
        main_layout.addWidget(wdg_right)

        qs = QSlider(Qt.Vertical)
        qs.setValue(50)
        lay.addWidget(qs)
        qsc = QScrollBar(Qt.Vertical)
        qsc.setValue(50)
        lay.addWidget(qsc)



    def createRightContent(self):
        lay = QVBoxLayout(self.topright)

        qs = QSlider(Qt.Horizontal)
        qs.setValue(50)
        lay.addWidget(qs)
        qpb = QProgressBar()
        qpb.setValue(50)
        lay.addWidget(qpb)
        qsc = QScrollBar(Qt.Horizontal)
        qsc.setValue(50)
        lay.addWidget(qsc)

        lay.addStretch()


    def createBasicLayout(self):
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(QMargins(0, 0, 0, 0))

        self.topleft = QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)
        self.topleft.setMinimumWidth(300)

        self.topright = QFrame(self)
        self.topright.setMinimumWidth(250)
        self.topright.setMaximumWidth(450)
        self.topright.setFrameShape(QFrame.StyledPanel)


        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setMaximumHeight(100)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.topleft)
        self.splitter1.addWidget(self.topright)

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.setContentsMargins(QMargins(0, 0, 0, 0))
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.bottom)

        self.hbox.addWidget(self.splitter2)
        self.setLayout(self.hbox)
