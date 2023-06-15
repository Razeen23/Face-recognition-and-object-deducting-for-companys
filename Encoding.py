import cv2 as cv
import face_recognition
import pickle  #using pickle for serializing the Python object and store it in a file or database
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# the key is more important because it's contains Confidential information
cred = credentials.Certificate("service_account_key.json")

# the {} for because it's a JSON file it have the key and values
firebase_admin.initialize_app(cred, {'databaseURL': "https://company-attendance-database-default-rtdb.firebaseio.com/",
                                     'storageBucket': "company-attendance-database.appspot.com"})#for the storage



#import employee to list
folder_image = 'Images'
image_path = os.listdir(folder_image)#set the path to image_path by using operating system.list Directly

emp_img_list = []
emp_ids = []

for path in image_path: #for loop to append the action to list
    emp_img_list.append(cv.imread(os.path.join(folder_image,path)))
    emp_ids.append(os.path.splitext(path)[0])#Separate the .png from the name and take the number

    # print(path)
    # print(os.path.splitext(path)[0])
# print(emp_ids)
# print(emp_img_list)
# print(len(action_list))

    # file_name = (os.path.join(folder_image,path))
    file_name = f'{folder_image}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)




def con_encoding(image_list):
    encode_list = []

    for img in image_list:

        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0] #take the encode using face_encodings take the first element [0]
        encode_list.append(encode)

    return encode_list

con_encoding_list = con_encoding(emp_img_list)
# print(con_encoding_list)
#con_encoding_list with emp_ids to store
encode_with_id = [con_encoding_list,emp_ids]
# print(encode_with_id)

file = open('ecodeing_file','wb')
pickle.dump(encode_with_id,file)
# print(file.read())
file.close()

















