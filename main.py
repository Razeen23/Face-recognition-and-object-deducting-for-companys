
import os
import cv2 as cv

cap = cv.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# print(cap.isOpened())
img_background = cv.imread('Resources1/MacBook Air - 1.jpg')

#import actions to list and resize it
folder_action = 'Resources1/Actions'
action_path = os.listdir(folder_action)

action_list = []
desired_width, desired_height = 405, 625
#
for path in action_path:
    action_img = cv.imread(os.path.join(folder_action, path))

# this line of code(next 3 line) is not necessary, i code it because i get some error  because of my macbook but
    # for best we can use it , in macbook there is a file called .DS_Store ,it Automatically creates
        # when we create a folder , it will Affect our program
    if action_img is None:
        print(f"failed to load image: {path}")
        continue

    # action_img = cv.resize(action_img, (405,625))
    action_img = cv.resize(action_img, (desired_width, desired_height))

    action_list.append(action_img)

#  print(action_path[1])
#  print(len(action_list))
#  print(action_path)

while True:
    success, webcam = cap.read()

    img_background[273:273 + 480, 103:103 + 640] = webcam
#   img_background[173:173 + 610, 830:830 + 390] = action_list[0]
    img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[0]

    cv.imshow('face attendance', img_background)
#   cv.imshow('web cam', webcam)

    cv.waitKey(1)







