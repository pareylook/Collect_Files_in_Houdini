from PySide import QtCore, QtGui
import hou, os, shutil

class Ui_collectfiles(object):
    def setupUi(self, collectfiles):
        collectfiles.setObjectName("collectfiles")
        collectfiles.resize(295, 193)
        self.verticalLayout_2 = QtGui.QVBoxLayout(collectfiles)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtGui.QComboBox(collectfiles)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.gr_filepath = QtGui.QGroupBox(collectfiles)
        self.gr_filepath.setObjectName("gr_filepath")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gr_filepath)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ln_filepath = QtGui.QLineEdit(self.gr_filepath)
        self.ln_filepath.setObjectName("ln_filepath")
        self.horizontalLayout_2.addWidget(self.ln_filepath)
        self.btn_browsefile = QtGui.QToolButton(self.gr_filepath)
        self.btn_browsefile.setObjectName("btn_browsefile")
        self.horizontalLayout_2.addWidget(self.btn_browsefile)
        self.verticalLayout.addWidget(self.gr_filepath)
        self.gr_parm = QtGui.QGroupBox(collectfiles)
        self.gr_parm.setObjectName("gr_parm")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gr_parm)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ln_parm = QtGui.QLineEdit(self.gr_parm)
        self.ln_parm.setObjectName("ln_parm")
        self.horizontalLayout_3.addWidget(self.ln_parm)
        self.verticalLayout.addWidget(self.gr_parm)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.btn_collect = QtGui.QPushButton(collectfiles)
        self.btn_collect.setObjectName("btn_collect")
        self.verticalLayout_2.addWidget(self.btn_collect)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(collectfiles)
        QtCore.QMetaObject.connectSlotsByName(collectfiles)

    def retranslateUi(self, collectfiles):
        collectfiles.setWindowTitle(QtGui.QApplication.translate("collectfiles", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("collectfiles", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("collectfiles", "Texture", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("collectfiles", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.gr_filepath.setTitle(QtGui.QApplication.translate("collectfiles", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_browsefile.setText(QtGui.QApplication.translate("collectfiles", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.gr_parm.setTitle(QtGui.QApplication.translate("collectfiles", "Custom Parametr", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_collect.setText(QtGui.QApplication.translate("collectfiles", "Collect", None, QtGui.QApplication.UnicodeUTF8))


class UICollect (QtGui.QWidget, Ui_collectfiles):
    def __init__(self):
        super(UICollect, self).__init__()
        self.setupUi(self)

        # connectors
        self.btn_browsefile.clicked.connect(self.setFilePath)
        self.comboBox.currentIndexChanged.connect(self.updateUI)
        self.btn_collect.clicked.connect(self.collectFiles)

        # start
        self.updateUI()




    def updateUI(self):
        self.gr_parm.setEnabled(self.comboBox.currentIndex() == 2)




    def setFilePath(self):
        d = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        self.ln_filepath.setText(d)





    def copyProcess(self, arg_parm_name, arg_path):
        if arg_path:
            nodes = hou.selectedNodes()
            for n in nodes:
                child = n.children()
                for c in child:
                    if c.parm(arg_parm_name):
                        oldPath = c.parm(arg_parm_name).eval()
                        newPath = os.path.join(arg_path, os.path.basename(oldPath))
                        if os.path.exists(newPath):
                            os.remove(newPath)
                        shutil.copy2(oldPath, newPath)
                        c.parm(arg_parm_name).set(os.path.join(arg_path, os.path.basename(oldPath)))

    def collectFiles(self):
        if self.comboBox.currentIndex() == 0:
            self.copyProcess('file', self.ln_filepath.text())

        elif self.comboBox.currentIndex() == 1:
            self.copyProcess('map', self.ln_filepath.text())

        elif self.comboBox.currentIndex() == 2:
            self.copyProcess(self.ln_parm.text(), self.ln_filepath.text())

