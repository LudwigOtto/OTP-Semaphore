from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login_helper = LoginManager(app)
login_helper.login_view = 'login'

from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail
from datetime import datetime, timedelta
from forms import LoginForm, SignupForm, OathForm
from user import User
from rdb import RDB
from mail import FMSG
import subprocess

redis_helper = RDB()
mail_handler = Mail(app)
msg = FMSG()
msg.set_sender(app.config['ADMIN'])

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        return render_template("index.html")
    print(request.cookies.get("session"))
    print(current_user.email)
    print(current_user.id)
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
        user = redis_helper.query_user_by_mail(form.email.data)
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return render_template('login.html', form=form)
        if not redis_helper.is_valid_user(user):
            flash('This account is blocked!!!')
            return redirect(url_for('index'))

        #Password confirmed
        login_user(load_user(user.id), duration=timedelta(minutes=5))
        proc = subprocess.Popen(['java', 'TOTP'], stdout=subprocess.PIPE)
        code = proc.stdout.readline()
        print(code)
        resp = make_response(redirect(url_for('oath')))
        req_key = request.cookies.get("session")
        key = req_key[-32:]
        resp.set_cookie(key='s_id', value=key)
        redis_helper.add_user_liveSession(user, code, key)

        msg.set_recipient([user.email])
        mail_handler.send(msg.send_code(code))
        return resp
    return render_template('login.html', form=form)

@login_required
@app.route('/oath', methods=['GET', 'POST'])
def oath():
    form = OathForm()
    if form.validate_on_submit():
        code = form.code.data
        key = request.cookies.get("s_id")
        print(key)
        res = redis_helper.check_user_liveSession(current_user, code, key)
        if res == 1:
            return redirect(url_for('index'))
        elif res == -1:
            flash("Either you or other(s) are masquerader. The account is blocked now!")
            redis_helper.block_user(current_user)
            msg.set_recipient([current_user.email])
            current_time = datetime.utcnow().strftime("%I:%M%p on %B %d, %Y UTC")
            mail_handler.send(msg.send_alert(current_time))
            return redirect(url_for('logout'))
        else:
            flash("Wrong verification code!!!")
    return render_template('oath.html', form=form)

@login_helper.user_loader
def load_user(user_id):
    user = redis_helper.query_user_by_id(user_id)
    return user

@app.route('/logout')
def logout():
    key = request.cookies.get("s_id")
    redis_helper.drop_user_liveSession(current_user, key)
    logout_user()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('s_id', expires=0)
    return resp

if __name__ == "__main__":
    app.run()
