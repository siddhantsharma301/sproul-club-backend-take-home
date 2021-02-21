from mongoengine import *

connect('sproulclub')

class Student(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    textbooks = ListField(required=True)