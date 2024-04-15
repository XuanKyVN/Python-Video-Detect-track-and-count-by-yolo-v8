from collections import defaultdict
import time
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from math import sqrt


# Load the YOLOv8 model
yolo_path = 'C:/Users/Admin/PythonLession/YoloModel/yolov8s.pt'
video_path = 'C:/Users/Admin/PythonLession/pic/people1.mp4'
PolygonPoints =[[[169, 478], [1258, 478], [1258, 752], [169, 752], [169, 478]], [[267, 233], [695, 233], [695, 427], [267, 427], [267, 233]]]
Linepoints = [[[67, 598, 574, 364], [723, 710, 1118, 392]]]

def minDistance( A, B, E):
    # vector AB
    AB = [None, None];
    AB[0] = B[0] - A[0];
    AB[1] = B[1] - A[1];

    # vector BP
    BE = [None, None];
    BE[0] = E[0] - B[0];
    BE[1] = E[1] - B[1];

    # vector AP
    AE = [None, None];
    AE[0] = E[0] - A[0];
    AE[1] = E[1] - A[1];
    # Variables to store dot product
    # Calculating the dot product
    AB_BE = AB[0] * BE[0] + AB[1] * BE[1];
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1];

    # Minimum distance from
    # point E to the line segment
    reqAns = 0;

    # Case 1
    if (AB_BE > 0):
        # Finding the magnitude
        y = E[1] - B[1];
        x = E[0] - B[0];
        reqAns = sqrt(x * x + y * y);
    # Case 2
    elif (AB_AE < 0):
        y = E[1] - A[1];
        x = E[0] - A[0];
        reqAns = sqrt(x * x + y * y);

    # Case 3
    else:
        # Finding the perpendicular distance
        x1 = AB[0];
        y1 = AB[1];
        x2 = AE[0];
        y2 = AE[1];
        mod = sqrt(x1 * x1 + y1 * y1);
        reqAns = abs(x1 * y2 - y1 * x2) / mod;
    return reqAns




def countingLinepolygon(video_path,yolo_path,Linepoints,PolygonPoints):
    model=YOLO(yolo_path)
    cap = cv2.VideoCapture(video_path)
    track_history = defaultdict(lambda: [])
    obcross = 30 # 8 pxel, when object near the line, calculator start couting
    #crossed_objects = {}
    crossed_objects = [{},{},{},{},{},{}, {},{},{},{}]
    crossed_objects1 = [{},{},{},{},{},{}, {},{},{},{}]

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            frame = cv2.resize(frame, (1400, 800))
            results = model.track(frame, persist=True, classes=[0]) # Tracking Car only
            if results[0].boxes.id != None:
                boxes = results[0].boxes.xywh.cpu()
                #print(boxes)
                track_ids = results[0].boxes.id.int().cpu().tolist()
                # Visualize the results on the frame
                #annotated_frame = results[0].plot()
                annotated_frame =frame
                pos_label_P=[]
                pos_label_P_count=[]

                counterP = [0,0,0,0,0,0,0,0,0,0]
                counterL = [0,0,0,0,0,0,0,0,0,0]
                pos_label_L=[]

                # Plot the tracks
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))  # x, y center point
                    # Draw Center point of object
                    cv2.circle(annotated_frame, (int(x), int(y)), 1, (0, 255, 0), 2)
                    if len(track) > 30:  # retain 90 tracks for 90 frames
                        track.pop(0)
                    # Check Center point (x,y) in the polygon or not. ( In =1; Out =-1, On polygon =0)
                    #--------------POLYGON COUNTER-----------------------------
                    if len(PolygonPoints)>0:
                        for idx,data in enumerate(PolygonPoints):
                            pts = np.asarray(data, dtype=np.int32)  # Convert to Numpy Array
                            pts = pts.reshape(-1, 1, 2)
                            cv2.polylines(annotated_frame, [pts], True, (255, 0, 0), 2)
                            dist = cv2.pointPolygonTest(pts, (int(x), int(y)), False)

                            if dist==1:

                                cv2.circle(annotated_frame, (int(x), int(y)), 8, (0, 0, 255), 2)
                                cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)),
                                              (0, 255, 0), 2)
                                counterP[idx] += 1
                                # Remember Object Passing the area
                                if track_id not in crossed_objects1[idx]:
                                    crossed_objects1[idx][track_id] = True

                                # --------------------Final - Polygon --------------------------------------
                                # print(counter)
                        temp = []
                        temp1=[]
                        for data in PolygonPoints:
                            #print(data)
                            temp.append(data[0])
                            temp1.append(data[3])
                        pos_label_P=temp.copy()
                        pos_label_P_count =temp1.copy()
                        #print(pos_label_P)

                    # ---------------------------------------------------------------

                    #-----------------------LINE --------COUNTER-----------

                    distance = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if len(Linepoints) > 0:
                        for data in Linepoints:
                            for idx,data1 in enumerate(data):

                                A0 = [data1[0], data1[1]]
                                B0 = [data1[2], data1[3]]
                                E = [x, y]
                                distance[idx] = minDistance(A0, B0, E)
                                cv2.line(annotated_frame,(data1[0],data1[1]),(data1[2],data1[3]),(255,0,0),2)
                                if distance[idx] < obcross:  # Assuming objects cross horizontally
                                    if track_id not in crossed_objects[idx]:
                                        crossed_objects[idx][track_id] = True
                                    # Annotate the object as it crosses the line
                                    cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)),
                                                  (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                                    cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)),
                                                  (int(x + w / 2), int(y + h / 2)),
                                                  (0, 255, 0), 2)

                                counterL[idx] = len(crossed_objects[idx])
                        #print(crossed_objects)
                        #print(counterL)

                        temp=[]
                        #print(len(Linepoints))
                        for data in Linepoints:
                            #print(data)
                            for data1 in data:
                                temp.append([data1[0],data1[1]])
                        pos_label_L=temp.copy()
                        #print(pos_label_L)'''
                #-----------------Final Display -----Polygon---------And Line------
                
                

                for idx, pos in enumerate(pos_label_L):
                    #print(pos)
                    cv2.putText(annotated_frame, "Count In Line: " + str(counterL[idx]), (pos[0], pos[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 0), 2)
                    #print(counterL[idx])
                #--------------------------------------------------

                for index, pos in enumerate(pos_label_P):
                    cv2.putText(annotated_frame, "Count In Region: " + str(counterP[index]), (pos[0], pos[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)
                    #print(index)
                    #print(pos)
                    cv2.putText(annotated_frame, "Count Obj pass: " + str(len(crossed_objects1[index])), (pos[0], pos[1]+150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


                #-------------------------------------------------

                cv2.putText(annotated_frame, "Xuan Ky Automation", (550, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (235, 255, 0), 2)

                # Display the annotated frame
                cv2.imshow("YOLOv8 Tracking", annotated_frame)
                # DELAY THE FRAME FOR CHECKING COUNTER
                time.sleep(0.1)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        else:
            print("Video Completed")
            break

    cap.release()
    cv2.destroyAllWindows()





countingLinepolygon(video_path,yolo_path,Linepoints,PolygonPoints)

