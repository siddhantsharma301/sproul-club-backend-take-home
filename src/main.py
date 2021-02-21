"""
Start server and stuff here
"""
import json
import pymongo

def get_textbook_name(id, db):
    return db['textbooks'].find_one({"id": id})

# Set up client and database
client = pymongo.MongoClient("localhost", 27017)
if 'sproulclub' not in client.list_database_names():
    database = client['sproulclub']

    # Load data into textbooks collection
    textbooks = database['textbooks']
    with open('/Users/siddhant/Documents/code/sproul-club-backend-take-home/textbooks.json') as file:
        file_data = json.load(file)
    textbooks.insert_many(file_data)

    # Load data into students collection
    students = database['students']
    with open('/Users/siddhant/Documents/code/sproul-club-backend-take-home/students.json') as file:
        file_data = json.load(file)
    students.insert_many(file_data)
else:
    database = client['sproulclub']

email = "oski@berkeley.edu"
password = "oskilovescal123"
student = database['students'].find_one({"email": email, "password": password})

textbook_id = 2

if textbook_id not in student['textbooks'] and database['textbooks'].find_one({"id": textbook_id}):
    print("here")

