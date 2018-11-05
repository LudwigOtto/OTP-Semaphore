from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
#from redis import Redis, RedisError
from forms import LoginForm, SignupForm
from user import User
from rdb import RDB
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
#redis = Redis()
redis_helper = RDB()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(form.email.data)
        user.set_password(form.password_0.data)
        redis_helper.add_user(user)
        flash("Thanks for Sign Up")
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
