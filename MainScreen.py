import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import pyqtSignal  # cach 2


from video import Ui_Video
from input import Ui_Input


class Video(QMainWindow):

    def __init__(self):
        super(Video, self).__init__()
        self.uic = Ui_Video()
        self.uic.setupUi(self)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a menu called "File"
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Create actions for menu items
        open_action = QAction("Selectvideo", self)
        save_action = QAction("Run_Detect", self)
        exit_action = QAction("Exit", self)

        # Connect the menu actions to functions that do something
        open_action.triggered.connect(self.showwin2)
        save_action.triggered.connect(self.Runprogram)
        exit_action.triggered.connect(self.close)

        # Add the actions to the "File" menu
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Adds a separator line in the menu
        file_menu.addAction(exit_action)

    def showwin2(self):
        print("Open file menu item selected")
        # self.hide() # or self.close()

        self.window2 = Input()
        # self.uic.pushButton.connect(self.showwindow1)
        self.window2.show()
        self.mainwin=Video()
        self.window2.datasend.connect(self.mainwin.getdata)

    def Runprogram(self):
        print("Run file menu item selected")


    def getdata(self, the_signal):
        # self.edit.setText(the_signal)
        print("receive data from screen 1")
        print(the_signal)



    def exitwin(self):
        self.close()


class Input(QMainWindow):

    datasend = QtCore.pyqtSignal(str)  # Send String to others window screen/ Class

    def __init__(self, index=0):
        super(Input, self).__init__()
        self.uic = Ui_Input()
        self.uic.setupUi(self)

        self.uic.ButtonClose.clicked.connect(self.exitwin)
        self.uic.ButtonAddsource.clicked.connect(self.send)

    def send(self):
        self.datasend.emit("Send Data String to next screen")
    def exitwin(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Video()
    main_win.show()

    windowno2 = Input()

    windowno2.datasend.connect(main_win.getdata)
    sys.exit(app.exec())


'''
from PyQt5 import QtWidgets
from win1 import Ui_MainWindow
from win2 import Ui_MainWindow2

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.closeAction = QtWidgets.QAction('Closing', self)
        self.menuBar().addAction(self.closeAction)
        self.openWin2Action = QtWidgets.QAction('Open Win #2', self)
        self.menuBar().addAction(self.openWin2Action)

        self.closeAction.triggered.connect(self.close)
        self.openWin2Action.triggered.connect(self.openWin2)

    def openWin2(self):
        self.win2 = Window2()
        self.win2.show()


class Window2(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

'''