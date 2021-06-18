# We will write script to capture Dataset for traing the model 
import cv2
import os
import sys

try:
    if(sys.argv[1] == "rock" or sys.argv[1] == "paper" or sys.argv[1] == "scissors" or sys.argv[1] == "none"):
        label_name = sys.argv[1]
    else:
        print("label_name can only be rock, paper or scissors")

    if(sys.argv[2].isdecimal()):
        num_samples = int(sys.argv[2])
    else:
        print("num_samples can only be a number")
except:
    print("Please enter arguments as follows : python capture.py label_name num_samples")
    print("To Start Press A and to quit press Q")
    exit(-1)

MAIN_DIR = './dataset'
CLASS_DIR = os.path.join(MAIN_DIR,label _name) 

try:
    os.mkdir(MAIN_DIR)
except FileExistsError:
    pass
try:
    os.mkdir(CLASS_DIR)
except FileExistsError:
    print("Warning: {} directory already exists.".format(CLASS_DIR))
    print("Warning: All images are stored in the same directory")

cap = cv2.VideoCapture(0)
start = False
count = 0 

while True:
    retval,frame = cap.read()               # frame is a image
    frame = cv2.flip(frame,1)
    if not retval:                          # Continues until cap.read() returns anything
        continue


    if count == num_samples:                # breaks loopp when all required images are captured
        break

    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)

    if start:
        crop = frame[100:500,100:500]
        save_path =  os.path.join(CLASS_DIR,'{}.jpg'.format(count+1))
        cv2.imwrite(save_path,crop)
        count = count+1
    
    #To Display frame and information while capturing
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.putText(frame,"Collecting {}".format(count),(5,50),font,0.6,(255,0,0),2,cv2.LINE_AA)
    cv2.namedWindow("Gathering {} data".format(label_name), cv2.WINDOW_KEEPRATIO)
    cv2.imshow("Gathering {} data".format(label_name),frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break
    
print("\n{} image(s) saved to {}".format(count, CLASS_DIR))
cap.release()
cv2.destroyAllWindows()
