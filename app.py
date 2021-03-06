from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User ,FeedBack
from forms import UserForm , loginForm , FeedbackForm
from sqlalchemy.exc import IntegrityError
import os
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///user_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY' , 'hello')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def nothing():
    return redirect('/register')

@app.route('/register' , methods = ['POST' , 'GET'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        error = False
        if User.query.filter_by(username = username).first():
            error = True
            flash('invalid username')
        if User.query.filter_by(email = email).first():
            error = True
            flash('invalid email')
        if error:
            return render_template('register.html',form = form)
        new_user = User.register(username, password, first_name, last_name, email)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = username
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html' , form = form)

@app.route('/users/<username>' ,  methods = ['POST' , 'GET'])
def info_user(username):
    if 'user_id' not in session:
        flash('Unautorized')
        return redirect('/')
    user = User.query.get(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        fb = FeedBack(title = title , content = content , username = username)
        db.session.add(fb)
        db.session.commit()
        return redirect(f'/users/{username}')

    else:
        return render_template('user_info.html' , user = user , form = form)



@app.route('/login', methods = ['POST' , 'GET'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authentication(username , password)
        if user:
            flash('Welcome Back!')
            session['user_id'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors.append('Invalid username/password')
    return render_template('login.html' , form=form)

@app.route('/secret')
def secret():
    if 'user_id' not in session:
        flash('please Login first!')
        return redirect('/')
    return render_template('secret.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    flash("Goodbye!")
    return redirect('/')