import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# the key is more important because it's contains Confidential information
cred = credentials.Certificate("service_account_key.json")

# the {} for because it's a JSON file it have the key and values
firebase_admin.initialize_app(cred, {'databaseURL': "https://company-attendance-database-default-rtdb.firebaseio.com/"})

ref = db.reference('Employees')

#create a JSON file inside a JSON file
data = {
    "123":
        {
            "name":"Elon",
            "age":39,
            "salary":500000.00,
            "role":" manager",
            "employee_id":123,
            "total_attendance":80,
            "last_attendance_time":"2023-06-15 00:00:00"

        },
    "456":
        {
            "name":"Mark",
            "age":51,
            "salary":600000.00,
            "role":"full stack developer",
            "employee_id":456,
            "total_attendance":90,
            "last_attendance_time":"2023-06-15 00:00:00"

        },
    "789":
        {
            "name":"Sundar",
            "age":51,
            "salary":400000.00,
            "role":"tester",
            "employee_id":789,
            "total_attendance":85,
            "last_attendance_time":"2023-06-15 00:00:00"

        },
    "2309":
        {
            "name":"Razeen",
            "age":22,
            "salary":15000.00,
            "role":"python developer",
            "employee_id":2309,
            "total_attendance":75,
            "last_attendance_time":"2023-06-15 00:00:00"

        }
       }

#in loop set the value to realtime database using the key
for key,value in data.items():
    ref.child(key).set(value)







