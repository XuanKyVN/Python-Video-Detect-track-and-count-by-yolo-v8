from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QMenu, QAction,QPushButton,QInputDialog,QFileDialog,QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from ultralytics import YOLO
from input import Ui_Input

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.videosource = ""
        self.pretrainsource = ""



    @pyqtSlot(dict)
    def receivedata(self, dict_data):
        print(" data recived at QThread Classes: ")
        print(dict_data)
        self.videosource =dict_data["v"]
        self.pretrainsource = dict_data["pt"]
        print(self.videosource)
        print(self.pretrainsource)

    def run(self):
        #print(self.data)
        #yolo_path = 'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'
        # Open the video file
        #video_path = "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
        yolo_path =self.pretrainsource
        video_path=self.videosource
        if yolo_path!="" and video_path!="":
            model = YOLO(yolo_path)
            cap = cv2.VideoCapture(video_path)

                # Loop through the video frames
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()
                # frame=cv2.resize(frame,(480,640))
                if success:

                    # Run YOLOv8 tracking on the frame, persisting tracks between frames
                    # results = model.track(frame, persist=True,show=True)
                    # results = model.track(frame, persist=True)
                    results = model.predict(frame)
                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()
                    self.change_pixmap_signal.emit(annotated_frame)

                else:
                    # Break the loop if the end of the video is reached
                    print(" no video file")
                    cap.release()
        else:
            print(" Please input the source video or pretrain model")


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()



class Input(QMainWindow):

    datasend = pyqtSignal(dict)  # send dict Yolo and Video to Class Qthread

    def __init__(self, index=0):
        super(Input, self).__init__()
        self.uic = Ui_Input()
        self.uic.setupUi(self)
        self.uic.Button_browse_Video.clicked.connect(self.filedialog1)
        self.uic.Button_pretrain.clicked.connect(self.filedialog2)

        self.uic.ButtonClose.clicked.connect(self.close)
        self.uic.ButtonAddsource.clicked.connect(self.senddata)
        self.videosource=""
        self.pretrainsource=""

        self.mainwin = App()
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.mainwin.update_image)

    def filedialog1(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Model (*.mp4 )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames)
            if filenames:
                # self.file_list.addItems([str(Path(filename)) for filename in filenames])
                self.uic.source_video.setText(str(Path(filenames[0])))
                self.videosource = self.uic.source_video.text()


    def filedialog2(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Model (*.pt )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames)
            if filenames:
                # self.file_list.addItems([str(Path(filename)) for filename in filenames])
                self.uic.source_pretrain_file.setText(str(Path(filenames[0])))
                #self.videopath.emit(str(Path(filenames[0])))
                self.pretrainsource = self.uic.source_pretrain_file.text()

    def senddata(self):
        data = {"v": self.videosource, "pt":self.pretrainsource}
        self.datasend.emit(data)
        #print(data)

class App(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 1200
        self.display_height = 800
        self.setGeometry(30,30,1000,600) #x,y w,h

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.button1 = QPushButton('Select source')
        self.button2 = QPushButton('Start')
        self.button3 =QPushButton('Stop')



        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        vbox.addWidget(self.button3)


        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        #--------------------------
        self.button1.clicked.connect(self.selectsource)
        self.button2.clicked.connect(self.start)
        self.button3.clicked.connect(self.close)

        #--------------------------
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

    def selectsource(self):
        self.window1 = Input()
        self.window1.show()
        self.thread = VideoThread()
        self.window1.datasend.connect(self.thread.receivedata)






    def start(self):
            self.thread.start()



    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)


    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()


    sys.exit(app.exec_())