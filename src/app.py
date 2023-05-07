import os
import secrets
from datetime import datetime
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.widgets import PasswordInput
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text
import sqlite3


class SignUpForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    gender = RadioField('Gender',
                        choices=[('M', 'Male'), ('F', 'Female')],
                        validators=[DataRequired()])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')],
                      validators=[DataRequired()])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')],
                        validators=[DataRequired()])
    profile_photo = FileField('Profile Image',
                              validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    
    have_breakfast = RadioField('Do you have breakfast Everyday?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    exercise = RadioField('Do you Exercise?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    meditate = RadioField('Do you Meditate?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    intro_extro = RadioField('Are you an introvert or extrovert?',
                                choices=[('introvert', 'Introvert'), ('extrovert', 'Extrovert')],
                                validators=[DataRequired()])
    smoke = RadioField('Do you Smoke?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    drink = RadioField('Do you Drink?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    present_hostel = SelectField('Present Hostel',
                                 choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                 validators=[DataRequired()])
    preferred_hostel = SelectField('Preferred Hostel',
                                   choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                   validators=[DataRequired()])
    content = StringField('About You',
                          validators=[DataRequired(), Length(min=50, max=1200)])
    password = PasswordField('Password',
                             validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     widget=PasswordInput(hide_value=False))
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already Taken!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use!')
    
    
class SignInFormEmail(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
    
class SignInFormUsername(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    gender = RadioField('Gender',
                        choices=[('M', 'Male'), ('F', 'Female')],
                        validators=[DataRequired()])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')],
                      validators=[DataRequired()])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')],
                        validators=[DataRequired()])
    profile_photo = FileField('Profile Image',
                              validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    
    have_breakfast = RadioField('Do you have breakfast Everyday?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    exercise = RadioField('Do you Exercise?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    meditate = RadioField('Do you Meditate?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    intro_extro = RadioField('Are you an introvert or extrovert?',
                                choices=[('introvert', 'Introvert'), ('extrovert', 'Extrovert')],
                                validators=[DataRequired()])
    smoke = RadioField('Do you Smoke?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    drink = RadioField('Do you Drink?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    present_hostel = SelectField('Present Hostel',
                                 choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                 validators=[DataRequired()])
    preferred_hostel = SelectField('Preferred Hostel',
                                   choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                   validators=[DataRequired()])
    content = StringField('About You',
                          validators=[DataRequired(), Length(min=50, max=1200)])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already Taken!')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use!')
    

class SearchForm(FlaskForm):
    username = StringField('Username')
    gender = RadioField('Your Gender:',
                                choices=[('M', 'Male'), ('F', 'Female')],
                                validators=[DataRequired()])
    preferred_hostel = RadioField('Preferred Hostel:',
                                choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')])
    submit = SubmitField('Search')
    
# Setup for flask app and database
app = Flask(__name__)
app.config['SECRET_KEY'] = '1974bf4e181357512bf418984285ad45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signInEmail'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.String(3), nullable=False)
    course = db.Column(db.String(3), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    profile_photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    have_breakfast = db.Column(db.String(1), nullable=False)
    exercise = db.Column(db.String(1), nullable=False)
    meditate = db.Column(db.String(1), nullable=False)
    intro_extro = db.Column(db.String(9), nullable=False)
    smoke = db.Column(db.String(1), nullable=False)
    drink = db.Column(db.String(1), nullable=False)
    present_hostel = db.Column(db.String(5), nullable=False)
    preferred_hostel = db.Column(db.String(5), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    roommate_pref1 = db.Column(db.Integer, nullable=False, default=-1)
    roommate_pref2 = db.Column(db.Integer, nullable=False, default=-1)
    roommate_pref3 = db.Column(db.Integer, nullable=False, default=-1)
    
    # followers = db.relationship('User', backref='added_me', lazy=True)
    # following = db.relationship('User', backref='i_added', lazy=True)
    
    def __repr__(self):
        # We are not printing content as it can be very long and the data may look messy
        return f"User('{self.id}', '{self.name}', '{self.username}', '{self.email}', '{self.year}', '{self.course}', '{self.gender}', '{self.profile_photo}', '{self.have_breakfast}', '{self.exercise}', '{self.meditate}', '{self.intro_extro}', '{self.smoke}', '{self.drink}', '{self.present_hostel}', '{self.preferred_hostel}', '{self.password}', '{self.roommate_pref1}', '{self.roommate_pref2}', '{self.roommate_pref3}')"

# SQLITE_DB = "/instance/database.db"

# This function takes argument as a string form of query to be executed > executes the query and returns the result obtained
# example:
# query_db("""CREATE TABLE IF NOT EXISTS songs (id, name, img, artist, album, duration, UNIQUE(id));""")

def query_db(*args, **kw_args):
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute(*args, **kw_args).fetchall()
    con.commit()
    cur.close()
    con.close()
    return result

@app.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('Main-Pages/index.html')
    else:
        return redirect(url_for('signInEmail'))
    # return render_template('Main-Pages/index.html')


def save_profile_picture(form_picture):
    random_text = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_text + file_extension
    picture_path = os.path.join(app.root_path, 'static/Media/profile_pictures', picture_filename)
    form_picture.save(picture_path)
    return picture_filename


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        picture_filename = 'default.jpg'
        if form.profile_photo.data:
            temp_picture_filename = save_profile_picture(form.profile_photo.data)
            picture_filename = temp_picture_filename
            
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    year=form.year.data,
                    course=form.course.data,
                    gender=form.gender.data,
                    profile_photo=picture_filename,
                    have_breakfast=form.have_breakfast.data,
                    exercise=form.exercise.data,
                    meditate=form.meditate.data,
                    intro_extro=form.intro_extro.data,
                    smoke=form.smoke.data,
                    drink=form.drink.data,
                    present_hostel=form.present_hostel.data,
                    preferred_hostel=form.preferred_hostel.data,
                    password=hashed_password,
                    # datetime=form.datetime.data,
                    content=form.content.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created Successfully {form.username.data}! Now you can Log In!', 'success')
        return redirect(url_for('signInEmail'))
    return render_template('Forms/signUp.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/signInEmail', methods=['GET', 'POST'])
def signInEmail():
    form = SignInFormEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else render_template('Main-Pages/index.html')
        else:
            flash('Login unsucessful! Please check your credentials!', 'danger')
    return render_template('Forms/signInEmail.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signInEmail'))

@app.route('/user-info', methods=['GET', 'POST'])
def user_info():
    pref1 = User.query.filter_by(username=current_user.username).first().roommate_pref1
    pref2 = User.query.filter_by(username=current_user.username).first().roommate_pref2
    pref3 = User.query.filter_by(username=current_user.username).first().roommate_pref3
    user1 = User.query.filter_by(id=pref1).first()
    user2 = User.query.filter_by(id=pref2).first()
    user3 = User.query.filter_by(id=pref3).first()
    return render_template('Main-Pages/UserInfo.html', user=current_user, pref1=user1, pref2=user2, pref3=user3)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.profile_photo.data:
            picture_file = save_profile_picture(form.profile_photo.data)
            current_user.profile_photo = picture_file
            
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.year = form.year.data
        current_user.course = form.course.data
        current_user.have_breakfast = form.have_breakfast.data
        current_user.exercise = form.exercise.data
        current_user.meditate = form.meditate.data
        current_user.intro_extro = form.intro_extro.data
        current_user.smoke = form.smoke.data
        current_user.drink = form.drink.data
        current_user.present_hostel = form.present_hostel.data
        current_user.preferred_hotel = form.preferred_hostel.data
        current_user.content = form.content.data
        
        db.session.commit()
        flash('Account Info successfully updated!', 'success')
        return redirect(url_for('user-info'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.year.data = current_user.year
        form.course.data = current_user.course
        form.have_breakfast.data = current_user.have_breakfast
        form.exercise.data = current_user.exercise
        form.meditate.data = current_user.meditate
        form.intro_extro.data = current_user.intro_extro
        form.smoke.data = current_user.smoke
        form.drink.data = current_user.drink
        form.present_hostel.data = current_user.present_hostel
        form.preferred_hostel.data = current_user.preferred_hostel
        form.content.data = current_user.content
        
    image_file = current_user.profile_photo
    return render_template('Forms/update.html', form=form, image_file=image_file)

# Use create an instance of UpdateForm() for the update page
# don't forget to add get and post request to the update page

# @login_required
# write all the routes here that require a login to access

# image_file = url_for('static', filename='/Media/profile_pictures' + current_user.profile_photo)
# render_template('<somefile.html>', image_file=image_file)

@app.route('/remove-pref-1', methods=['GET', 'POST'])
def remove_pref_1():
    current_user.roommate_pref_1 = -1
    return redirect(url_for('user_info'))

@app.route('/remove-pref-2', methods=['GET', 'POST'])
def remove_pref_2():
    current_user.roommate_pref_2 = -1
    return redirect(url_for('user_info'))

@app.route('/remove-pref-3', methods=['GET', 'POST'])
def remove_pref_3():
    current_user.roommate_pref_3 = -1
    return redirect(url_for('user_info'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        username=form.username.data
        year=form.year.data
        preferred_hostel = form.preferred_hostel.data
        course = form.course.data
        gender = form.gender.data
        query_str = f"SELECT * FROM User WHERE gender='{gender}'"
        if username:
            query_str += f" AND username='{username}'"
        if preferred_hostel:
            query_str += f" AND preferred_hostel='{preferred_hostel}'"
        if year:
            query_str += f" AND year='{year}'"
        if course:
            query_str += f" AND course='{course}'"
        query_str += ';'
        ans = query_db(query_str)
        # form.username.data = username
        # form.gender.data = gender
        # form.preferred_hostel.data = preferred_hostel
        # form.year.data = year
        # form.course.data = course
        return render_template('Main-Pages/search-page.html', form=form, display='t', users=ans)
    return render_template('Main-Pages/search-page.html', form=form, display='f')

@app.route('/show-all-users', methods=['GET', 'POST'])
def show_all_users():
    list_of_users = User.query.all()
    return render_template('Main-Pages/all-users.html', users=list_of_users)

@app.route('/open-user-profile/<string:username>', methods=['GET', 'POST'])
def open_user_profile(username):
    user=User.query.filter_by(username=username).first()
    return render_template('Main-Pages/other-user.html', user=user)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('Main-Pages/about.html')
    
if __name__ == '__main__':
    app.run(debug=True)