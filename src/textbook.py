from mongoengine import *

connect('sproulclub')

class Textbook(Document):
    book_id = IntField(required=True)
    name = StringField(required=True)
    author = StringField(required=True)