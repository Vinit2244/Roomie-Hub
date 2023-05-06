# Hackathon
This repository is for the members to collaborate and work on the ISS hackathon project.

Team Number: 60

Members:
    1. Ashwin Kumar
    2. Tanay Gad
    3. Vinit Mehta

# How to open our website
    -> Run the app.py python file in src folder

# Do:
    -> pip install flask-wtf
    -> pip install email_validator
    -> pip install flask-sqlalchemy
    -> pip install flask-bcrypt
    -> pip install flask-login

    # To create/initiate database:
        -> from app import app, db
        -> app.app_context().push()
        -> db.create_all()
        -> from app import User

    # To delete all the tables and database
        -> app.drop_all() / db.drop_all()