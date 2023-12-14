# This is the code to train the model on the images stored in the Images folder and then use the webcam to recognise wether the image is present in the Images folder or not.

# Imported all the packages and declared all necesary variables
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
import csv

def verify():
    path = "Images"
    images = []
    classNames = []
    myList = os.listdir(path)

    # Get all the images in the images list and the usernames in the classnames list
    for obj in myList:
        img = cv2.imread(f"{path}/{obj}")
        images.append(img)
        classNames.append(os.path.splitext(obj)[0])

    # Find the face encodings in each of the images and return it as a lsit
    def encodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    
    # Mark the attendance in a csv file
    def mark_attendance(name):
        date = datetime.now().strftime("%Y-%m-%d")
        # Get the file name with today's date
        dir_path = os.path.dirname(os.path.abspath(__file__))
        attendance_dir = os.path.join(dir_path,"Attendance")
        filename = os.path.join(attendance_dir,f"{date}.csv")

        # Check if the file exists
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                # If the file doesn't exist, write the header
                writer.writeheader()
            # Write the name and current time
            current_time = datetime.now().strftime("%H:%M:%S")
            writer.writerow({'Name': name, 'Time': current_time})

    encodeListKnown = encodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    start_time = time.time()  # Start time for the 10-second timeout

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # print(f"{name} logged in successfully")
                mark_attendance(name)
                cap.release()
                cv2.destroyAllWindows()
                return True,name

        if time.time() - start_time > 10:
            print("No faces matched within 10 seconds.")
            cap.release()
            cv2.destroyAllWindows()
            return False,'No match'

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
