import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
#model = YOLO('C:/Users/Admin/PythonLession/YoloModel/yolov8s.pt')
#yolo_path = 'C:/Users/Admin/PythonLession/yolo_dataset/best_carplate5.pt'
# Open the video file
#video_path = "C:/Users/Admin/PythonLession/pic/carplate6.mp4"
def detect_obj_video(video_path,yolo_path):
    model = YOLO(yolo_path)
    cap = cv2.VideoCapture(video_path)

# Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        #frame=cv2.resize(frame,(480,640))
        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            #results = model.track(frame, persist=True,show=True)
            #results = model.track(frame, persist=True)
            results = model.predict(frame)
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            #display(annotated_frame)
        else:
            # Break the loop if the end of the video is reached
            print(" no video file")
            cap.release()
            cv2.destroyAllWindows()
            break

    return annotated_frame

#def display(frame):
    #cv2.imshow("YOLOv8 Detecting", frame)
    #cv2.waitKey(10)

#frame = detect_obj_video(video_path,yolo_path)
