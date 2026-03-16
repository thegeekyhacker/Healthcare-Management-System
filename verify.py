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
        # Skip non-image files like desktop.ini, .DS_Store etc.
        if not obj.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img = cv2.imread(f"{path}/{obj}")
        if img is None:
            print(f"Warning: Could not load {obj}, skipping.")
            continue
        # Convert BGR to RGB immediately on load
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
        classNames.append(os.path.splitext(obj)[0])

    if not images:
        print("No valid images found in Images folder.")
        return False, 'No match'

    # Find the face encodings in each of the images and return it as a list
    def encodings(images):
        encodeList = []
        for i, img in enumerate(images):
            locs = face_recognition.face_locations(img)
            if not locs:
                print(f"Warning: No face detected in reference image for {classNames[i]}, skipping.")
                continue
            encode = face_recognition.face_encodings(img, locs)[0]
            encodeList.append(encode)
        return encodeList

    # Mark the attendance in a csv file
    def mark_attendance(name):
        date = datetime.now().strftime("%Y-%m-%d")
        dir_path = os.path.dirname(os.path.abspath(__file__))
        attendance_dir = os.path.join(dir_path, "Attendance")
        if not os.path.exists(attendance_dir):
            os.makedirs(attendance_dir)
        filename = os.path.join(attendance_dir, f"{date}.csv")

        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            current_time = datetime.now().strftime("%H:%M:%S")
            writer.writerow({'Name': name, 'Time': current_time})

    encodeListKnown = encodings(images)
    if not encodeListKnown:
        print("No faces could be encoded from reference images.")
        return False, 'No match'

    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False, 'No match'

    start_time = time.time()

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Could not read from webcam.")
            break

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
                mark_attendance(name)
                cap.release()
                cv2.destroyAllWindows()
                return True, name

        if time.time() - start_time > 10:
            print("No faces matched within 10 seconds.")
            cap.release()
            cv2.destroyAllWindows()
            return False, 'No match'

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    return False, 'No match'