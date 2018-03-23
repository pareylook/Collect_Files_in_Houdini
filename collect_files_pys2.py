from hutil.Qt.QtWidgets import *

import os, hou, shutil

class myWidget (QWidget):
    def __init__(self):
        super(myWidget, self).__init__()
        self.setProperty("houdiniStyle", True)
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.comboBox = QComboBox();
        self.comboBox.addItem("File")
        self.comboBox.addItem("Texture")
        self.comboBox.addItem("Custom")
        mainLayout.addWidget(self.comboBox)

        self.grpBox = QGroupBox("Type name parameter")
        self.grpBox.setEnabled(False)
        self.label_name = QLabel("Name")
        self.line_name = QLineEdit()
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_name)
        hbox.addWidget(self.line_name)
        self.grpBox.setLayout(hbox)
        mainLayout.addWidget(self.grpBox)
        self.button_collect = QPushButton("Collect")
        mainLayout.addWidget(self.button_collect)

        spacerItem = QSpacerItem(40, 400, QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainLayout.addItem(spacerItem)

        # connectors
        # self.btn_browsefile.clicked.connect(self.setFilePath)
        self.comboBox.currentIndexChanged.connect(self.updateUI)
        self.button_collect.clicked.connect(self.collectFiles)

    def updateUI (self):
        self.grpBox.setEnabled(self.comboBox.currentIndex()==2)
        # print (self.comboBox.currentIndex())

    def collectFiles(self):
        hipPath = hou.hipFile.path()
        # dirName = "collectGeo"

        if self.comboBox.currentIndex()==0:
            arg_parm_name = "file"
            dirName = "collectGeo"
        elif self.comboBox.currentIndex()==1:
            arg_parm_name = "map"
            dirName = "collectTex"
        elif self.comboBox.currentIndex()==2:
            arg_parm_name = self.line_name.text()
            dirName = "collect"

        dirPath = os.path.join(os.path.dirname(hipPath), dirName)
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        nodes = hou.selectedNodes()

        for n in nodes:
            child = n.children()
            for c in child:
                if c.parm(arg_parm_name):
                    oldPath = c.parm(arg_parm_name).eval()
                    if not os.path.basename(oldPath) == "default.bgeo":
                        newPath = os.path.join(dirPath, os.path.basename(oldPath))
                        if os.path.exists(newPath):
                            os.remove(newPath)
                        shutil.copy2(oldPath, newPath)
                        c.parm(arg_parm_name).set("$HIP/" + os.path.join(dirName, os.path.basename(oldPath)))



def createInterface():
    w = myWidget()
    return w
