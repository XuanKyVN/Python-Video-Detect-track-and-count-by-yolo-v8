import sys,cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QMenu, QAction,QPushButton,QInputDialog,QFileDialog
from PyQt5.QtGui import QPixmap, QPainter,QImage,QPen
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from ultralytics import YOLO
from videodetecttrackscreen import Ui_MainWindow




class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.data = ""
        self.video_path=""
        self.yolo_path=""
        self.Mode =0
        self.classes =[]

        #print(self.data)
    @pyqtSlot(dict)
    def receivedata(self, dict_data):
        # dict = {'classes': [1,5,3,6] , 'Mode': 0, 'v' : "C:/Users/Admin/PythonLession/pic/carplate6.mp4", 'pt':'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'}
        print(dict_data)
        self.video_path =dict_data["v"]
        self.yolo_path = dict_data['pt']
        self.Mode = dict_data['Mode']
        self.classes = dict_data['classes']

        print(self.video_path)
        print(self.yolo_path)
        print(self.Mode)
        print(self.classes)


    def run(self):
        video_path = self.video_path  # "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
        yolo_path = self.yolo_path #'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'
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
                    if self.Mode==0:
                        if self.classes == []:
                            results = model.predict(frame)
                        else:
                            results = model.predict(frame, classes=self.classes)
                        # Visualize the results on the frame

                    else:
                        if self.classes == []:
                            results = model.track(frame,persist=True)
                        else:
                            results = model.track(frame, persist=True,classes=self.classes)
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
        #self.wait()
        self.quit()
        self.terminate()


class MainWindow(QMainWindow):
    dataconfig = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        # ------------------------------------------------------
        self.disply_width = 1350
        self.display_height = 900
        #self.setGeometry(30, 30, 1000, 600)
        # create the label that holds the image
        self.uic.label_img.resize(self.disply_width, self.display_height)

        self.uic.PBInitiate.clicked.connect(self.selectVideo)
        self.uic.PBInitiate.clicked.connect(self.selectPretrain)

        self.uic.PBStart.clicked.connect(self.start)
        self.uic.PBPause.clicked.connect(self.pause)
        self.uic.PBExit.clicked.connect(self.close)


        #-------------------------------------------
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.dataconfig.connect(self.thread.receivedata)

        # ------------------------------------------------------
        self.classes=[]
        self.Mode = 0
        self.video_path =""
        self.pretrainpath =""


        #------------------------------------------------

    def start(self):
        if self.video_path != "" and self.pretrainpath != "":
            self.Mode = self.uic.Combo_Mode.currentIndex()
            data_in_classtxt = "," + self.uic.SelectClasses.text() + ","
            poscomma = []
            index = 0
            if self.uic.SelectClasses.text() == "":
                self.classes = []
            else:
                for i in data_in_classtxt:  # for element in range(0, len(string_name)):
                    if i == ',':  # print(string_name[element])
                        poscomma.append(index)
                    index += 1
                # print(poscomma)
                for j in range(0, len(poscomma) - 1):
                    if data_in_classtxt[poscomma[j] + 1:poscomma[j + 1]] != "":
                        self.classes.append(int(data_in_classtxt[poscomma[j] + 1:poscomma[j + 1]]))
            data = {'classes': self.classes, 'Mode': self.Mode, 'v': self.video_path, 'pt': self.pretrainpath}
            # print(data)
            self.dataconfig.emit(data)

            # ----------------------
            self.thread.start()
            # pass
            self.status = True
        else:
            print(" Please slect Video and pretrain Path")
            self.uic.Videopath_txt.setText("Please slect Video and pretrain Path")

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
                self.video_path =str(Path(filenames[0]))
                self.uic.Videopath_txt.setText(str(Path(filenames[0])))


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
                self.pretrainpath =str(Path(filenames[0]))
                self.uic.PretrainPathTxt.setText(str(Path(filenames[0])))

                names_classes=self.classesUpdate(self.video_path,self.pretrainpath)
                #print(names_classes)
                index=0
                for i in range(0, len(names_classes)-1):
                    self.uic.Classes_Txt.append(str(index) +"  "+ names_classes[i])
                    index+=1


    def closeEvent(self, event):
        self.thread.stop()
        #self.imgthread.stop()
        event.accept()

    def pause(self):
        self.thread.stop()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label_img.setPixmap(qt_img)



    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def classesUpdate(self, video_path,yolo_path):

        model = YOLO(yolo_path)
        if video_path != "" and yolo_path!="":
            cap = cv2.VideoCapture(video_path)
            # Loop through the video frames
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()
                # frame=cv2.resize(frame,(480,640))
                if success:
                    # results = model.track(frame, persist=True,show=True)
                    # results = model.track(frame, persist=True)
                    results = model.predict(frame)
                    names = results[0].names

                    names_classes = []
                    self.update_image(frame) # Update Image

                    self.uic.Classes_Txt.setText("")
                    for x in names.values():
                        # print(x)
                        names_classes.append(x)

                    break
        return names_classes



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())