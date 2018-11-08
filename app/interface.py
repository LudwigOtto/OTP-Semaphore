from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login_helper = LoginManager(app)
login_helper.login_view = 'login'

from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from forms import LoginForm, SignupForm
from user import User
from rdb import RDB

redis_helper = RDB()

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        resp = make_response(render_template('index.html'))
        return resp
    #if current_user.is_authenticated:
    #    return render_template('welcome.html')
    #expires = datetime.utcnow() + timedelta(minutes=5)
    #resp.set_cookie(key='name', value='I am cookie',expires=expires)
    #print(request.cookies.get("session"))
    #resp = make_response(render_template('index.html'))
    #return resp
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        if redis_helper.is_existed_user(form.email.data):
            flash("Account already existed")
            return redirect(url_for('signup'))
        #user.set_password(form.password_0.data)
        user = User(form.email.data)
        user.set_password(form.password_0.data)
        redis_helper.add_user(user)
        flash("Thanks for Sign Up")
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if not redis_helper.is_existed_user(form.email.data):
            flash("Account not existed")
            return redirect(url_for('login'))
        user = load_user(form.email.data)
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return render_template('login.html', form=form)
        login_user(user, duration=timedelta(minutes=5))
        #TODO:
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@login_helper.user_loader
def load_user(email):
    user = redis_helper.query_user(email)
    return user

if __name__ == "__main__":
    app.run()
