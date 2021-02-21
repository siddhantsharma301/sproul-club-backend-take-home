# Backend take home assignment for sproul.club - Spring 2021

## Due Date: Sunday, 2/21 11:59 AM PST (Noon)

<!-- MarkdownTOC autolink="true" -->

- [Objective](#objective)
- [Data models](#data-models)
- [Criteria](#criteria)
- [Library Docs](#library-docs)
- [Setting up tools and repository](#setting-up-tools-and-repository)
    - [Pre-setup](#pre-setup)
    - [Actual setup](#actual-setup)
- [Submitting your work](#submitting-your-work)

<!-- /MarkdownTOC -->

## Objective
Your objective is to build a REST API for a future website that allows students to maintain a list of textbooks from their school library and be able to share this list to their friends & family with ease.

For the sake of simplicity, instead of having you create the student account endpoints, we'll assume that there's only one student account that's pre-created. You can do this by making a new collection for students and adding a document for the test account, either via MongoDB Compass or programmatically.

The API should be able to do the following:

* **Textbook Management**
  * Let the student fetch their list of textbooks
  * Let the student add/remove more textbooks from a read-only collection of textbooks
* **Easy sharing**
  * Let the student share a QR code that embeds a link to their collection of textbooks.
  * This link will not expire and should return a list of the textbook names *only*.

Along with that, the API itself should follow the recommended guidelines:
* It should accept JSON where applicable and return JSON for responses
* It should return the appropriate errors for cases such as valid input, illegal operations, etc.

## Data models

While we'll let you decide how to precisely construct the data models, there are a few fields that are required:

Student (pre-created):
* Full name
* Email
* Password (hashed)
* List of Textbooks

Textbook:
* ID
* Name
* Author

## Criteria

We'll be considering the following questions when examining your code:
* Did you implement the business logic as stated in the criteria?
* Is there documentation included for using the API?
* How readable is your code? Are there comments for any parts of the code that look complicated?

You may use any extra tools, frameworks, generators, and/or dependencies to finish your task, as long as you use Flask for the REST framework and MongoDB as the database. This repo includes `flask`, `pymongo`, and `mongoengine` as dependencies to start out with, so you can check out the documentation below.

## Library Docs
* Flask - [docs](https://flask.palletsprojects.com/en/1.1.x/)
* PyMongo - [docs](https://pymongo.readthedocs.io/en/stable/)
* MongoEngine - [docs](https://docs.mongoengine.org/)

## Setting up tools and repository

### Pre-setup
* Make sure you have Python 3.6 or above installed
* Make sure that you have MongoDB Community Edition [installed](https://docs.mongodb.com/manual/administration/install-community/) and running.
  * I'd also recommend getting [MongoDB Compass](https://www.mongodb.com/products/compass), which is a handy tool to visually navigate through your databases, collections, and documents without going through the Mongo shell.

### Actual setup
1. Clone this repository and [create a virtual environment](https://docs.python.org/3.6/tutorial/venv.html)
2. Install the dependencies from `requirements.txt` with `pip install -r requirements.txt`
3. Start up the MongoDB service (either `mongod` or `mongod.exe`) [1]
4. Make a new database and import `textbooks.json` into a new collection for textbooks
5. Code it all out!!

[1] Note that the server will be hosted on `localhost` on port `27017` by default

## Submitting your work
When you're done, publish your code as a public repository on GitHub or any other preferred Git platform and email the link
to tejashah88@gmail.com. If you added any extra dependencies, be sure to add them to the requirements.txt with `pip freeze > requirements.txt`.
