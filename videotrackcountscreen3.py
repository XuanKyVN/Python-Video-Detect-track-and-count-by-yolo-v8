# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drawnpic2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1900, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_img = QtWidgets.QLabel(self.centralwidget)
        self.label_img.setGeometry(QtCore.QRect(0, 0, 1541, 945))
        self.label_img.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_img.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_img.setObjectName("label_img")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 890, 671, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(1550, 0, 340, 941))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(4)
        self.frame.setObjectName("frame")
        self.PBInitiate = QtWidgets.QPushButton(self.frame)
        self.PBInitiate.setGeometry(QtCore.QRect(20, 552, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PBInitiate.setFont(font)
        self.PBInitiate.setObjectName("PBInitiate")
        self.PBPause = QtWidgets.QPushButton(self.frame)
        self.PBPause.setGeometry(QtCore.QRect(20, 732, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PBPause.setFont(font)
        self.PBPause.setObjectName("PBPause")
        self.Videopath_txt = QtWidgets.QLineEdit(self.frame)
        self.Videopath_txt.setGeometry(QtCore.QRect(20, 12, 300, 31))
        self.Videopath_txt.setDragEnabled(False)
        self.Videopath_txt.setReadOnly(True)
        self.Videopath_txt.setObjectName("Videopath_txt")
        self.PretrainPathTxt = QtWidgets.QLineEdit(self.frame)
        self.PretrainPathTxt.setGeometry(QtCore.QRect(20, 52, 300, 31))
        self.PretrainPathTxt.setReadOnly(True)
        self.PretrainPathTxt.setObjectName("PretrainPathTxt")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(20, 822, 121, 16))
        self.label_3.setObjectName("label_3")
        self.PBExit = QtWidgets.QPushButton(self.frame)
        self.PBExit.setGeometry(QtCore.QRect(20, 885, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PBExit.setFont(font)
        self.PBExit.setObjectName("PBExit")
        self.PBStart = QtWidgets.QPushButton(self.frame)
        self.PBStart.setGeometry(QtCore.QRect(20, 682, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PBStart.setFont(font)
        self.PBStart.setObjectName("PBStart")
        self.ComboBox = QtWidgets.QComboBox(self.frame)
        self.ComboBox.setGeometry(QtCore.QRect(20, 782, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ComboBox.setFont(font)
        self.ComboBox.setObjectName("ComboBox")
        self.ComboBox.addItem("")
        self.ComboBox.addItem("")
        self.ComboBox.addItem("")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 92, 55, 16))
        self.label.setObjectName("label")
        self.PointData = QtWidgets.QLineEdit(self.frame)
        self.PointData.setGeometry(QtCore.QRect(20, 842, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.PointData.setFont(font)
        self.PointData.setObjectName("PointData")
        self.ButtonSet_region = QtWidgets.QPushButton(self.frame)
        self.ButtonSet_region.setGeometry(QtCore.QRect(220, 782, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ButtonSet_region.setFont(font)
        self.ButtonSet_region.setObjectName("ButtonSet_region")
        self.Combo_Mode = QtWidgets.QComboBox(self.frame)
        self.Combo_Mode.setGeometry(QtCore.QRect(20, 642, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Combo_Mode.setFont(font)
        self.Combo_Mode.setObjectName("Combo_Mode")
        self.Combo_Mode.addItem("")
        self.Combo_Mode.addItem("")
        self.Combo_Mode.addItem("")
        self.ClearDatapoint = QtWidgets.QPushButton(self.frame)
        self.ClearDatapoint.setGeometry(QtCore.QRect(210, 885, 111, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ClearDatapoint.setFont(font)
        self.ClearDatapoint.setObjectName("ClearDatapoint")
        self.Classes_Txt = QtWidgets.QTextEdit(self.frame)
        self.Classes_Txt.setGeometry(QtCore.QRect(20, 112, 300, 441))
        self.Classes_Txt.setReadOnly(True)
        self.Classes_Txt.setObjectName("Classes_Txt")
        self.SelectClasses = QtWidgets.QLineEdit(self.frame)
        self.SelectClasses.setGeometry(QtCore.QRect(20, 602, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SelectClasses.setFont(font)
        self.SelectClasses.setObjectName("SelectClasses")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1900, 26))
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
        self.label_2.setText(_translate("MainWindow", "COPY RIGHT FROM XUAN KY AUTOMATION   - DATE 24-3-2024"))
        self.PBInitiate.setText(_translate("MainWindow", "INITIATE PROGRAM"))
        self.PBPause.setText(_translate("MainWindow", "PAUSE_RESTART"))
        self.Videopath_txt.setPlaceholderText(_translate("MainWindow", "Video_Path"))
        self.PretrainPathTxt.setPlaceholderText(_translate("MainWindow", "Pretrain.pt / Best.pt"))
        self.label_3.setText(_translate("MainWindow", "Point X1,Y1, X2,Y2"))
        self.PBExit.setText(_translate("MainWindow", "EXIT"))
        self.PBStart.setText(_translate("MainWindow", "START DETECT OR TRACK"))
        self.ComboBox.setItemText(0, _translate("MainWindow", "Draw Line"))
        self.ComboBox.setItemText(1, _translate("MainWindow", "Draw Rectangle"))
        self.ComboBox.setItemText(2, _translate("MainWindow", "Draw Polyline"))
        self.label.setText(_translate("MainWindow", "CLASSES"))
        self.PointData.setPlaceholderText(_translate("MainWindow", "QPoint Data"))
        self.ButtonSet_region.setText(_translate("MainWindow", "SET REGION"))
        self.Combo_Mode.setItemText(0, _translate("MainWindow", "DETECT"))
        self.Combo_Mode.setItemText(1, _translate("MainWindow", "TRACK"))
        self.Combo_Mode.setItemText(2, _translate("MainWindow", "TRACK-COUNT"))
        self.ClearDatapoint.setText(_translate("MainWindow", "CLEAR"))
        self.SelectClasses.setPlaceholderText(_translate("MainWindow", "Ex: 1,3,5,8,2   ( if Detect all, dont put anything)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
