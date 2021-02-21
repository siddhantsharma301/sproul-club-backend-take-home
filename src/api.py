"""
API Endpoints
"""
import base64
import flask
import flask_pymongo
import io
import json
import pymongo
import qrcode
import requests

DB_PATH = '/Users/siddhant/Documents/code/sproul-club-backend-take-home/'

# Set up client and database
client = pymongo.MongoClient("localhost", 27017)
if 'sproulclub' not in client.list_database_names():
    database = client['sproulclub']

    # Load data into textbooks collection
    textbooks = database['textbooks']
    with open(DB_PATH + 'textbooks.json') as file:
        file_data = json.load(file)
    textbooks.insert_many(file_data)

    # Load data into students collection
    students = database['students']
    with open(DB_PATH + 'students.json') as file:
        file_data = json.load(file)
    students.insert_many(file_data)

else:
    database = client['sproulclub']

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/sproulclub"

database = flask_pymongo.PyMongo(app)


"""
A little homepage for the assignments
Acts as a how to use, what I did, etc.
"""
@app.route('/')
def home():
    return f"""<h1> sproul.club backend take home assignment</h1>
        <h2> How it works </h2>
        I set up my REST API to take requests at the `/api/`. Credentials such as student
        email and password are passed in through JSON, which are verified against the student and
        textbook collections in the MongoDB database. The endpoints were tested using Postman.
        <h2> API Endpoints </h2>
        <ul>
            <li> `/api/student-textbooks`: Fetch what textbooks a given student has. Need student's email and password </li>
            <li> `/api/add-student-textbooks`: Add textbook to student's list, if they do not already have textbook and textbook exists
                in textbook collection. Need student's email and password </li>
            <li> `/api/remove-student-textbooks`: Remove textbook from student's list, if they already have textbook. Need student's email and password </li>
            <li> `/api/student-textbooks-qrcode`: Generate QR Code of student's textbooks. Returns base64 encoded version of QR Code.
                Need student's email and password </li>
        </ul>
    """


"""
Get the textbook list for a given student

Params:
    email: str
        student's email
    password: str
        student's password

Returns:
JSON response with textbooks
"""
@app.route('/api/student-textbooks', methods=['GET'])
def get_student_textbooks():
    # Verify credentials, throw error as required
    request_data = flask.request.get_json()
    if request_data is None or request_data['email'] is None or request_data['password'] is None:
        return flask.jsonify({"message": "missing parameters, try again"})
    email = request_data['email']
    password = request_data['password']

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return flask.jsonify({"message": "student credentials not found"})

    # Create list of textbooks
    books = []
    for book in student['textbooks']:
        name = get_textbook_name(book)
        if name is not None:
            books.append(name)

    return flask.jsonify({"textbooks": books})


""" 
Put given textbook into student's list, if textbook exists
and is not already in student's list

Params: 
    email: str
        student's email 
    password: str
        student's password
    textbook_id: int
        textbook's id
"""
@app.route('/api/add-textbook-students', methods=['PATCH'])
def add_textbook_to_student():
    # Verify credentials, throw error as required
    request_data = flask.request.get_json()
    if request_data is None or request_data['email'] is None or request_data['password'] is None \
        or request_data["textbook_id"] is None:
        return flask.jsonify({"message": "missing parameters, try again"})
    email = request_data['email']
    password = request_data['password']
    textbook_id = request_data['textbook_id']

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return flask.jsonify({"message": "student credentials not found"})
    if not database.db['textbooks'].find_one({"id": textbook_id}):
        return flask.jsonify({"message": "database does not contain requested id"})

    # Add textbook if it doesn't exist in student's list already
    if textbook_id not in student['textbooks']:
        lst = student["textbooks"] + [textbook_id]
        lst.sort()
        replacement  = {
            "name": student["name"],
            "email": student["email"],
            "password": student["password"],
            "textbooks": lst
        }
        database.db['students'].replace_one({"email": email, "password": password}, replacement)
        return flask.jsonify({"message": "textbook successfully added to student"})
    else:
        return flask.jsonify({"message": "student already has requested textbook"})


""" 
Remove given textbook into student's list, if is already in student's list

Params: 
    email: str
        student's email 
    password: str
        student's password
    textbook_id: int
        textbook's id
"""
@app.route('/api/remove-textbook-students', methods=['PATCH'])
def remove_textbook_from_student():
    # Verify credentials, throw error as required
    request_data = flask.request.get_json()
    if request_data is None or request_data['email'] is None or request_data['password'] is None \
        or request_data["textbook_id"] is None:
        return flask.jsonify({"message": "missing parameters, try again"})
    email = request_data['email']
    password = request_data['password']
    textbook_id = request_data['textbook_id']

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return flask.jsonify({"message": "student credentials not found"})
    if not database.db['textbooks'].find_one({"id": textbook_id}):
        return flask.jsonify({"message": "database does not contain requested id"})

    # Remove textbook if in student's list already
    if textbook_id in student['textbooks']:
        lst = student["textbooks"]
        lst.remove(textbook_id)
        replacement  = {
            "name": student["name"],
            "email": student["email"],
            "password": student["password"],
            "textbooks": lst
        }
        database.db['students'].replace_one({"email": email, "password": password}, replacement)
        return flask.jsonify({"message": "textbook successfully removed from student"})
    else:
        return flask.jsonify({"message": "student does not have requested textbook"})
    

"""
Generate QR Code for given student
Takes student's credentials to verify their identity

Params:
    email: str
        student's email
    password: str
        student's password

Returns:
QR Code (in base64 format for JSON response)
"""
@app.route('/api/student-textbooks-qrcode', methods=['GET'])
def generate_qrcode():
    # Verify credentials, throw error as required
    request_data = flask.request.get_json()
    if request_data is None or request_data['email'] is None or request_data['password'] is None:
        return flask.jsonify({"message": "missing parameters, try again"})
    email = request_data['email']
    password = request_data['password']

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return flask.jsonify({"message": "student credentials not found"})

    # Create string of textbooks
    # books = ""
    # for book in student['textbooks']:
    #     name = get_textbook_name(book)
    #     if name is not None:
    #         books += name + "\n"

    # Generate QR code and convert to string
    qr = qrcode.make("localhost/" + student['name'].replace(" ", "%20") + "-textbooks")
    with io.BytesIO() as out:
        qr.save(out, format="png")
        qr_string = base64.b64encode(out.getvalue()).decode('UTF-8')
    create_textbook_list(student['name'])
    return flask.jsonify({"qrcode": qr_string})


"""
A page to host what textbooks a given student has

Params:
    name: str
        name of student
"""
@app.route('/<name>-textbooks', methods=['GET'])
def create_textbook_list(name):
    books = ""
    student = database.db['students'].find_one({"name": name})
    for book in student['textbooks']:
        name = database.db['textbooks'].find_one({"id": book})["name"]
        books += f"<li> {name} </li>"
    return f"""
        <h1> {name}'s Textbooks </h1>
        <ul>
    """ + books + "</ul>"


"""
Return textbook name for a given ID in given database

Params:
    id: int
        textbook id

Returns:
Name of textbook as string
"""
def get_textbook_name(id):
    return database.db['textbooks'].find_one({"id": id})['name']



if __name__ == "__main__":
    app.run(debug=True)
