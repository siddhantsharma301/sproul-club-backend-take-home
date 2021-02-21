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
        textbook collections in the MongoDB database. 
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
    db: Database
        database with students and textbooks

Returns:
JSON response with textbooks
"""
@app.route('/api/student-textbooks', methods=['GET'])
def get_student_textbooks():
    # Verify credentials, throw error as required
    request_data = flask.request.get_json()
    email = request_data['email']
    password = request_data['password']

    if email is None or password is None:
        return json.dumps({"error": "request does not contain either email or password"})

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return json.dumps({"error": "student credentials not found", "email": email, "password": password})

    # Create list of textbooks
    books = []
    for book in student['textbooks']:
        name = get_textbook_name(book)
        if name is not None:
            books.append(name)

    return json.dumps({"textbooks": books})


""" 
Put given textbook into student's list, if textbook exists
and is not already in student's list

Params: 
    email: str
        student's email 
    password: str
        student's password
    id: int
        textbook's id
    db: Database
        database with students and textbook
"""
@app.route('/api/add-textbook-students', methods=['PUT'])
def add_textbook_to_student():
    # Verify credentials, throw error as required
    email = request.args.get('email', None) 
    password = request.args.get('password', None)
    id = request.args.get('id', None)

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return json.dumps({"error": "student credentials not found"})

    if not student['textbooks'].contains(id) and database.db['textbooks'].find_one({"id": id}):
        student['textbooks']


""" 
Remove given textbook into student's list, if is already in student's list

Params: 
    email: str
        student's email 
    password: str
        student's password
    id: int
        textbook's id
    db: Database
        database with students and textbook
"""
@app.route('/api/add-textbook-students', methods=['PUT'])
def remove_textbook_from_student():
    # Verify credentials, throw error as required
    email = request.args.get('email', None) 
    password = request.args.get('password', None)
    id = request.args.get('id', None)

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return json.dumps({"error": "student credentials not found"})

    if not student['textbooks'].contains(id) and database.db['textbooks'].find_one({"id": id}):
        student['textbooks']
    

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
    email = request_data['email']
    password = request_data['password']

    student = database.db['students'].find_one({"email": email, "password": password})

    if student is None:
        return json.dumps({"error": "student credentials not found"})

    # Create string of textbooks
    books = ""
    for book in student['textbooks']:
        name = get_textbook_name(book)
        if name is not None:
            books += name + "\n"

    # Generate QR code and convert to string
    qr = qrcode.make(books)
    with io.BytesIO() as out:
        qr.save(out, format="png")
        qr_string = base64.b64encode(out.getvalue()).decode('UTF-8')

    return json.dumps({"qrcode": qr_string})


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
