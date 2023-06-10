import os
import cv2 as cv


cap = cv.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# print(cap.isOpened())
# img_background = cv.imread('Resources/background.png')
img_background = cv.imread('Resources1/MacBook Air - 1.jpg')


#import actions to list
folder_action = 'Resources1/Actions'
action_path = os.listdir(folder_action)#set the path to action_path by using operating system.list Directly

action_list = []
# action_list[1] = 'Resources1/Actions/101.jpg'
for path in action_path: #for loop to append the action to list
    action_list.append(cv.imread(os.path.join(folder_action, path)))

# print(action_path[1])
print(len(action_list))
# print(action_path)


while True:
    success, webcam = cap.read()

    img_background[273:273 + 480, 103:103 + 640] = webcam
    # img_background[180:180 + 610, 830:830 + 390] = action_list[1]

    cv.imshow('face attendance', img_background)
    # cv.imshow('web cam', webcam)
    cv.waitKey(1)
