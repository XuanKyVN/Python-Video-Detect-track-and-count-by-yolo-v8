import sys, cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction,QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

from ultralytics import YOLO
import numpy as np

# from PyQt5.QtCore import pyqtSignal  # cach 2
from pathlib import Path

from VideoDetection import detect_obj_video

from video import Ui_Video
from input import Ui_Input
#---------------------------------------------


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    checksignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.signal = None
        self.yolo_path=""
        self.video_path=""




    def run(self):
        #yolo_path = 'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'
        # Open the video file
        #video_path = "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
        if self.video_path!="" and self.yolo_path!="":
            model = YOLO(self.yolo_path)
            cap = cv2.VideoCapture(self.video_path)

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
                    cv2.waitKey(1)
                else:
                    # Break the loop if the end of the video is reached
                    print(" no video file")
                    cap.release()

    def getdata(self, the_signal):
        # self.edit.setText(the_signal)
        # print("receive data from screen 1")

        if the_signal!="" :
            self.checksignal.emit(True)
        else:
            self.checksignal.emit(False)

        self.signal = the_signal
        print(self.signal)
        self.video_path = self.signal['v']
        self.yolo_path = self.signal['pt']
        print(self.video_path)
        print(self.yolo_path)



    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


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


#------------------------------------------
        self.enable = False
    def startthread(self):
       # create the video capture thread
       if self.enable:
            self.thread = VideoThread()
            # connect its signal to the update_image slot
            self.thread.change_pixmap_signal.connect(self.update_image)
            # start the thread
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

    def getdata_start(self, signal):
        # self.edit.setText(the_signal)
        # print("receive data from screen 1")
        print(signal)
        self.enable= signal


#--------------------------------------------
    def showwin2(self):
        #print("Open file menu item selected")
        # self.hide() # or self.close()
        self.window1 =Video()

        self.window2 = Input()
        # self.uic.pushButton.connect(self.showwindow1)
        self.window2.show()
        self.window3=VideoThread()

        self.window2.datasend.connect(self.window3.getdata)

        self.window3.checksignal.connect(self.window1.startthread)

    def Runprogram(self):
        print("Run file menu item selected")


    '''def getdata(self, the_signal):
        # self.edit.setText(the_signal)
        #print("receive data from screen 1")
        print(the_signal)
        video_path = the_signal['v']
        yolo_path = the_signal['pt']
        print(yolo_path)'''



    def exitwin(self):
        self.close()



class Input(QMainWindow):

    datasend = pyqtSignal(dict)  # Send String to others window screen/ Class

    def __init__(self, index=0):
        super(Input, self).__init__()
        self.uic = Ui_Input()
        self.uic.setupUi(self)

        self.uic.ButtonClose.clicked.connect(self.exitwin)
        self.uic.ButtonAddsource.clicked.connect(self.send)
        self.uic.Button_browse_Video.clicked.connect(self.openFileNamesvideo)
        self.uic.Button_pretrain.clicked.connect(self.openFileNamespretrain)
    def openFileNamesvideo(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Model (*.mp4 )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames)
            if filenames:
                #self.file_list.addItems([str(Path(filename)) for filename in filenames])
                self.uic.source_video.setText(str(Path(filenames[0])))

    def openFileNamespretrain(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\image')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Model (*.pt )")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            #print(filenames)
            if filenames:
                #self.file_list.addItems([str(Path(filename)) for filename in filenames])
                self.uic.source_pretrain_file.setText(str(Path(filenames[0])))


    def send(self):
        sourcevideo = self.uic.source_video.text()
        sourcept = self.uic.source_pretrain_file.text()
        data = {"v": sourcevideo, "pt":sourcept}

        self.datasend.emit(data)
    def exitwin(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Video()
    main_win.show()

    windowno2 = Input()
    window3 =VideoThread()
    windowno2.datasend.connect(window3.getdata)

    window3.checksignal.connect(main_win.startthread)

    sys.exit(app.exec())
