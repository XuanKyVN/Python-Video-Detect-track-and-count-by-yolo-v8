from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QMenu, QAction,QPushButton,QInputDialog,QFileDialog
from PyQt5.QtGui import QPixmap
import sys,os
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from ultralytics import YOLO


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.data = ""
        self.videopath=""
        self.pretrainpath=""


        #print(self.data)
    def receivedata(self, stringdata):
        #print(stringdata)
        #self.data=stringdata

        file_path = stringdata
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1]
            if file_extension.lower() == ".mp4":
                self.videopath =file_path
                print(" receive video path: " + self.videopath)
            if file_extension.lower() == ".pt":
                self.pretrainpath =file_path
                print(" receive PT path: " + self.pretrainpath)

        '''
        # importing the modules
            import os
            import pathlib
            path = 'D:/test.txt'
            result = os.path.splitext(path)
            print('Extension:', result[1][1:])
            print('Extension:', pathlib.Path('D:/test.txt').suffix[1:])
            #https://www.tutorialspoint.com/How-to-extract-file-extension-using-Python#:~:text=pathlib%20module&text=The%20attribute%20suffix%20on%20the,in%20addition%20to%20the%20root.
            OR
            import pathlib
            path = pathlib.Path('D:\Work TP.py')
            print('Parent:', path.parent)
            print('NameOfFile:', path.name)
            print('Extension:', path.suffix)
        '''

    def run(self):

        yolo_path = self.pretrainpath #'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'
        # Open the video file
        video_path = self.videopath# "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
        if yolo_path != "" and video_path!="":
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
            print(" Please input Video path and pretrain path")

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    videopath = pyqtSignal(str)
    pretrainpath = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 1200
        self.display_height = 800
        self.setGeometry(30,30,1000,600)

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.button1 =QPushButton('SelectSourceFile')
        self.button2 = QPushButton('Start')
        self.button3 =QPushButton('Stop')
        #self.button4 =QPushButton('SelectPretrain')






        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.button1)
        #vbox.addWidget(self.button4)
        vbox.addWidget(self.button2)
        vbox.addWidget(self.button3)


        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        #--------------------------

        self.button1.clicked.connect(self.selectVideo)
        self.button1.clicked.connect(self.selectPretrain)

        self.button2.clicked.connect(self.start)
        self.button3.clicked.connect(self.close)

        #--------------------------
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

        self.videopath.connect(self.thread.receivedata)
        self.pretrainpath.connect(self.thread.receivedata)

    def start(self):
            self.thread.start()

    def selectVideo(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("VideoFile (*.mp4 )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames)
            if filenames:
                # self.file_list.addItems([str(Path(filename)) for filename in filenames])
                #self.uic.source_pretrain_file.setText(str(Path(filenames[0])))
                self.videopath.emit(str(Path(filenames[0])))

    def selectPretrain(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("PretrainFile (*.pt )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames
            if filenames:
                # self.file_list.addItems([str(Path(filename)) for filename in filenames])
                # self.uic.source_pretrain_file.setText(str(Path(filenames[0])))
                self.pretrainpath.emit(str(Path(filenames[0])))




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