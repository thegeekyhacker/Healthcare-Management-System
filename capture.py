# This is the code to capture the images for reference when and comparing and will be used while registering new users.
import cv2
import os
def capture_image(username):
    # Get the current wrking directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # Set the images to be stored at the Images folder
    img_dir = os.path.join(dir_path,"Images")
    # If Images folder does not exit, create it
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    cap = cv2.VideoCapture(0)   #Initialise the capturing device
    # 0 is used for default webcam
    # If you have more than one camera attached then change the index according to your needs
    # Check wether the webcam is successfully opened or not.
    if not cap.isOpened():
        print("Error: Could not open the webcam")
        exit()
    while True:
        ret, frame = cap.read()  #Capture a frame from the webcam feed
        if ret == False:         #If no frames are captured break out of the loop
            print("Error: Could not read a frame")
            break
        # Display the captured frame 
        cv2.imshow('Webcam Feed',frame)
        # Wait for the user to press a key to capture the image
        key = cv2.waitKey(1)
        # If the 's' key is pressed save the image as ajpg file
        if key == ord('s'):
            img_name = os.path.join(img_dir,f"{username}.jpg")
            cv2.imwrite(img_name,frame)
            print(f"Image saved as {img_name}")
            break
        # If the 'q' key is pressed, exit the program
        if key == ord('q'):
            break
    # Release the webcam
    cap.release()
    # Close the OpenCV windows
    cv2.destroyAllWindows()
# capture_image("utkarsh")