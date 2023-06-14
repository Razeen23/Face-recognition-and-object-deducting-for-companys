
import os
import pickle
import numpy as np
import cv2 as cv
import face_recognition
import cvzone as cz

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

#load the encoed file
print('loading file started...')

file = open('ecodeing_file','rb')
encode_with_id = pickle.load(file)
file.close()

con_encoding_list,emp_ids = encode_with_id
# print(emp_ids,con_encoding_list)
# file.read()
print('loading file ended...')


while True:
    success, webcam = cap.read()

    img_small = cv.resize(webcam,(0,0),None,0.25,0.25)#compress the images just because it take of memory to run
    img_small = cv.cvtColor(img_small, cv.COLOR_BGR2RGB)

    face_current = face_recognition.face_locations(img_small)#face location fine the Exact face area so we don't need to scan the whole img
    encode_face = face_recognition.face_encodings(img_small,face_current)#now we compare the face and encode data



    img_background[273:273 + 480, 103:103 + 640] = webcam
#   img_background[173:173 + 610, 830:830 + 390] = action_list[0]
    img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[1]

    for encodeFace,faceLocation in zip(encode_face,face_current):
        matches = face_recognition.compare_faces(con_encoding_list,encodeFace)
        face_dis = face_recognition.face_distance(con_encoding_list,encodeFace)

        # print('face matches',matches)
        # print('face distance',face_dis)

        match_index = np.argmin(face_dis) #argmin means argument minimum
        # print('match index ',match_index) #it gives the matching index

        if matches[match_index]:
            # print('face is recognized')
            print(emp_ids[match_index])
            # cv.rectangle(img_background,b)
            y1 , x2 , y2 , x1 = faceLocation
            y1 , x2 , y2 , x1 = y1*4 , x2*4 , y2*4 , x1*4

            bbox = 55+x1 ,162+y1 , x2-x1 , y2 - y1
            img_background = cz.cornerRect(img_background,bbox,rt=1)



    cv.imshow('face attendance', img_background)
#   cv.imshow('web cam', webcam)

    cv.waitKey(1)







