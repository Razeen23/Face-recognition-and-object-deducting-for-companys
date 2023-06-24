
import os
import pickle
import time

import numpy as np
import cv2 as cv
import face_recognition
import cvzone as cz

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

from datetime import datetime

# the key is more important because it's contains Confidential information
cred = credentials.Certificate("service_account_key.json")

# the {} for because it's a JSON file it have the key and values
firebase_admin.initialize_app(cred, {'databaseURL': "https://company-attendance-database-default-rtdb.firebaseio.com/",
                                     'storageBucket': "company-attendance-database.appspot.com"})#for the storage

bucket = storage.bucket()

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

action_type = 0
counter = 0
id = -1
img_employee = []


while True:
    success, webcam = cap.read()

    img_small = cv.resize(webcam,(0,0),None,0.25,0.25)#compress the images just because it take of memory to run
    img_small = cv.cvtColor(img_small, cv.COLOR_BGR2RGB)

    face_current = face_recognition.face_locations(img_small)#face location fine the Exact face area so we don't need to scan the whole img
    encode_face = face_recognition.face_encodings(img_small,face_current)#now we compare the face and encode data


    img_background[273:273 + 480, 103:103 + 640] = webcam
#   img_background[173:173 + 610, 830:830 + 390] = action_list[0]
    img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[action_type]

    if face_current:

        for encodeFace,faceLocation in zip(encode_face,face_current):
            matches = face_recognition.compare_faces(con_encoding_list,encodeFace)
            face_dis = face_recognition.face_distance(con_encoding_list,encodeFace)

            # print('face matches',matches)
            # print('face distance',face_dis)

            match_index = np.argmin(face_dis) #argmin means argument minimum
            # print('match index ',match_index) #it gives the matching index

            if matches[match_index]:
                # print('face is recognized')
                # print(emp_ids[match_index])
                # cv.rectangle(img_background,b)
                y1 , x2 , y2 , x1 = faceLocation
                y1 , x2 , y2 , x1 = y1*4 , x2*4 , y2*4 , x1*4 #we multiplay with 4 because we compress it 1/4 befour (line 58)

                # the box around the face
                bbox = 100 + x1, 255 + y1, x2 - x1, y2 - y1
                img_background = cz.cornerRect(img_background, bbox, rt=0)

                ##try to use cv2 but it's not fit properly it can we fix but i'm happy with cvzone layout
                ##img_background = cv.rectangle(img_background, (200 + x1,355 + y1), (x2 - x1, y2 -y1), (2, 300, 2), 2)

                id = emp_ids[match_index]
                if counter == 0:
                    counter = 1
                    action_type = 1

        if counter != 0:

            if counter == 1:
                emp_info = db.reference(f'Employees/{id}').get()#geting the data from the real time database Employees
                print(emp_info)

                blob = bucket.get_blob(f'Images/{id}.jpg')#getting the image from the database storage
                # print(blob)
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                img_employee = cv.imdecode(array,cv.COLOR_BGRA2BGR)#convert the img type and assign the value to img_employee


                date_time_object = datetime.strptime(emp_info['last_attendance_time'],
                                                    "%Y-%m-%d %H:%M:%S")

                seconds_gap = (datetime.now()-date_time_object).total_seconds()
                print(seconds_gap)

                salary = int(emp_info['salary'])
                total_attendance = int(emp_info['total_attendance'])

                current_salary = (salary/30) * total_attendance
                # print(current_salary)

                if seconds_gap > 20 :
                # if seconds_gap > 50400:
                #update the data to the attendance
                    ref = db.reference(f'Employees/{id}')
                    emp_info['total_attendance'] += 1 #adding one to the attendance
                    ref.child('total_attendance').set(emp_info['total_attendance'])  # and update in database

                    salary = int(emp_info['salary'])
                    total_attendance = int(emp_info['total_attendance'])
                    current_salary = (salary / 30) * total_attendance
                    # print(current_salary)

                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    emp_info['current_month_salary'] = current_salary  # adcing the current salary
                    ref.child('current_month_salary').set(emp_info['current_month_salary'])#update in database

                else:
                    action_type = 3
                    counter = 0
                    img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[action_type]

                print(emp_info['current_month_salary'])

            if action_type != 3:

                if 10<counter<20:
                    action_type = 2

                img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[action_type]

                if counter<=10:

                    cv.putText(img_background,str(emp_info['total_attendance']),(1143,254),
                                cv.FONT_HERSHEY_TRIPLEX,0.7,(255,255,255),1)

                    cv.putText(img_background, str(emp_info['employee_id']), (1022, 600),
                               cv.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 1)

                    # cv.putText(img_background, str(emp_info[('salary'/30)*'total_attendance']), (1057, 727),
                    #            cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
                    cv.putText(img_background, str(emp_info['current_month_salary']), (1057, 727),
                               cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)

                    cv.putText(img_background, str(emp_info['name']), (940, 254),
                               cv.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 1)

                    cv.putText(img_background, str(emp_info['role']), (1017, 665),
                               cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), 1)

                    img_employee_resized = cv.resize(img_employee, (216, 216))

                    img_background[306:306 + 216, 919:919 + 216] = img_employee_resized
                    # img_background[310:310 + 216, 917:917 + 216] = img_employee

                    time.sleep(5)

                counter+=1 #once it Recognise the face it updates the data

                if counter>=20:
                    counter = 0
                    action_type = 0
                    emp_info = []
                    img_employee = []
                    img_background[173:173 + desired_height, 823:823 + desired_width] = action_list[action_type]
    else:
        action_type = 0
        counter = 0

    cv.imshow('face attendance', img_background)
#   cv.imshow('web cam', webcam)

    cv.waitKey(1)






