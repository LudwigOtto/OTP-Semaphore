from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm
from user import User
from rdb import RDB
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
redis_helper = RDB()

@app.route('/')
@app.route('/index')
def index():
    redis_helper.debug()
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(form.email.data)
        if redis_helper.is_existed_user(user):
            flash("Account already existed")
            return redirect(url_for('signup'))
        user.set_password(form.password_0.data)
        redis_helper.add_user(user)
        flash("Thanks for Sign Up")
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

@app.route('/login', method=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.email.data)
        if not redis_helper.is_existed_user(user):
            flash("Account not existed")
            return redirect(url_for('login'))
        user.set_password(form.password_0.data)
        if not redis_helper.verify_user(user):
            flash('Invalid password')
            return render_template('login.html', form=form)
        login_user(user)
        #TODO:
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('index')
        #return redirect(next_page)
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run()
