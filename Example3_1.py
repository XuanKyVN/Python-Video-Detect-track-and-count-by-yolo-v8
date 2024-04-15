import cv2
import sys
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

#pyqtSignal = Signal
#pyqtSlot = Slot

class VideoContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Video'
        self.left = 100
        self.top = 100
        self.fwidth = 1000
        self.fheight = 600
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        # update image
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.fwidth, self.fheight)
        self.resize(1000, 600)

        # create a label
        self.label = QLabel(self)
        self.label.resize(1000, 600)

        self.th = Thread()
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        self.show()

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()

    def run(self):
        self.isRunning = True
        path = "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(path)

        while self.isRunning:
            ret, frame = cap.read()
            #frame = cv2.resize(frame,(1000,600))
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                #p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                p = convertToQtFormat.scaled(1000, 600, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


    def stop(self):
        self.isRunning = False
        self.quit()
        self.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoContainer()
    sys.exit(app.exec())