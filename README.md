# ROOMIEHUB - ISS Hackathon Project

## Team Number: 60

## Project Context:

This project was developed as a part of a 24-hour hackathon at the end of our Introduction to Software Systems course in the second semester.

### Team Members:

1. Vinit Mehta : Backend + Frontend
2. Ashwin Kumar : Frontend
3. Tanay Gad : Frontend

## Project Overview

**Name of Site:** ROOMIEHUB

### How to Open the Website:
- Run the `app.py` python file in the `src` folder.

### Installation Steps:
1. `pip install flask-wtf`
2. `pip install email_validator`
3. `pip install flask-sqlalchemy`
4. `pip install flask-bcrypt`
5. `pip install flask-login`

### Packages Used:
- os
- secrets
- flask
- flask_wtf
- wtforms
- wtforms.validators
- flask_wtf.file
- wtforms.widgets
- flask_sqlalchemy
- flask_bcrypt
- flask_login
- sqlalchemy

## Features Implemented:

1. **Signin/Signup:**
   - Create an account with a unique username and email with the required details.
   - Password is initially hidden and can be seen using show password.

2. **Search:**
   - Search based on username and add filters on a variety of parameters.

3. **Profile Page:**
   - Displays your profile with an option to change details and the people you are following.
   - You can remove people you are following from here.

4. **Followers Page:**
   - Displays people who you follow.

5. **Discover Page:**
   - List of all the users who have registered.

## Database Initialization:

To create/initiate the database run the following commands on python inside the shell in the `src` folder:
```python
from app import app, db
app.app_context().push()
db.create_all()
from app import User
```

## File Structure

.
├── README.md
└── src
    ├── app.py
    ├── instance
    │   └── database.db
    ├── __pycache__
    │   └── app.cpython-310.pyc
    ├── static
    │   ├── CSS
    │   │   ├── about.css
    │   │   ├── all-users.css
    │   │   ├── discover.css
    │   │   ├── form.css
    │   │   ├── header-footer.css
    │   │   ├── index.css
    │   │   ├── other-user.css
    │   │   ├── profile-page.css
    │   │   ├── search.css
    │   │   ├── signin.css
    │   │   ├── signup.css
    │   │   └── user-info.css
    │   └── Media
    │       ├── ashwin.png
    │       ├── full_logo-no-bg.png
    │       ├── full_logo.png
    │       ├── just_logo-no-bg.png
    │       ├── just_logo.png
    │       ├── main_wp.jpg
    │       ├── profile_pictures
    │       │   ├── ...
    │       ├── right.png
    │       ├── tanay.png
    │       ├── vinit.png
    │       └── wrong.png
    └── templates
        ├── Forms
        │   ├── signInEmail.html
        │   ├── signUp.html
        │   └── update.html
        ├── Layouts
        │   ├── form-layout.html
        │   └── main-layout.html
        └── Main-Pages
            ├── about.html
            ├── all-users.html
            ├── discover.html
            ├── followers.html
            ├── index.html
            ├── other-user.html
            ├── profiles.html
            ├── search-page.html
            └── UserInfo.html

Feel free to modify or enhance the documentation as needed. Good luck with your hackathon project!