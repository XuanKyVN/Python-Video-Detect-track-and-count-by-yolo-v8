# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drawnpic1.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1726, 1005)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_img = QtWidgets.QLabel(self.centralwidget)
        self.label_img.setGeometry(QtCore.QRect(20, 20, 1350, 900))
        self.label_img.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_img.setObjectName("label_img")
        self.PBExit = QtWidgets.QPushButton(self.centralwidget)
        self.PBExit.setGeometry(QtCore.QRect(1410, 820, 300, 41))
        self.PBExit.setObjectName("PBExit")
        self.Classes_Txt = QtWidgets.QTextEdit(self.centralwidget)
        self.Classes_Txt.setGeometry(QtCore.QRect(1410, 110, 300, 431))
        self.Classes_Txt.setReadOnly(True)
        self.Classes_Txt.setObjectName("Classes_Txt")
        self.SelectClasses = QtWidgets.QLineEdit(self.centralwidget)
        self.SelectClasses.setGeometry(QtCore.QRect(1410, 610, 300, 31))
        self.SelectClasses.setObjectName("SelectClasses")
        self.PBStart = QtWidgets.QPushButton(self.centralwidget)
        self.PBStart.setGeometry(QtCore.QRect(1410, 700, 300, 41))
        self.PBStart.setObjectName("PBStart")
        self.Combo_Mode = QtWidgets.QComboBox(self.centralwidget)
        self.Combo_Mode.setGeometry(QtCore.QRect(1410, 660, 300, 22))
        self.Combo_Mode.setObjectName("Combo_Mode")
        self.Combo_Mode.addItem("")
        self.Combo_Mode.addItem("")
        self.PBPause = QtWidgets.QPushButton(self.centralwidget)
        self.PBPause.setGeometry(QtCore.QRect(1410, 760, 300, 41))
        self.PBPause.setObjectName("PBPause")
        self.PBInitiate = QtWidgets.QPushButton(self.centralwidget)
        self.PBInitiate.setGeometry(QtCore.QRect(1410, 550, 300, 41))
        self.PBInitiate.setObjectName("PBInitiate")
        self.Videopath_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.Videopath_txt.setGeometry(QtCore.QRect(1410, 0, 300, 31))
        self.Videopath_txt.setDragEnabled(False)
        self.Videopath_txt.setReadOnly(True)
        self.Videopath_txt.setObjectName("Videopath_txt")
        self.PretrainPathTxt = QtWidgets.QLineEdit(self.centralwidget)
        self.PretrainPathTxt.setGeometry(QtCore.QRect(1410, 40, 300, 31))
        self.PretrainPathTxt.setReadOnly(True)
        self.PretrainPathTxt.setObjectName("PretrainPathTxt")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1410, 90, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 930, 671, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1726, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_img.setText(_translate("MainWindow", "VIDEO SCREEN"))
        self.PBExit.setText(_translate("MainWindow", "EXIT"))
        self.SelectClasses.setPlaceholderText(_translate("MainWindow", "Ex: 1,3,5,8,2   ( if Detect all, dont put anything)"))
        self.PBStart.setText(_translate("MainWindow", "START PROGRAM"))
        self.Combo_Mode.setItemText(0, _translate("MainWindow", "DETECT"))
        self.Combo_Mode.setItemText(1, _translate("MainWindow", "TRACK"))
        self.PBPause.setText(_translate("MainWindow", "PAUSE_RESTART"))
        self.PBInitiate.setText(_translate("MainWindow", "INITIATE PROGRAM"))
        self.Videopath_txt.setPlaceholderText(_translate("MainWindow", "Video_Path"))
        self.PretrainPathTxt.setPlaceholderText(_translate("MainWindow", "Pretrain.pt / Best.pt"))
        self.label.setText(_translate("MainWindow", "CLASSES"))
        self.label_2.setText(_translate("MainWindow", "COPY RIGHT FROM XUAN KY AUTOMATION   - DATE 24-3-2024"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
