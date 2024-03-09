from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, UserDataForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.DataVisualization import calculate_bmr, calculate_calorie_needs, calculate_macros_protein, calculate_macros_carbs, calculate_macros_fat, calculate_weight_loss_plan



@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", title = "Home", values = User.query.first()) # will add



@app.route("/view")
def view():
    return render_template("view.html", values = User.query.all())

@app.route("/info")
def info():
    weeks_to_goal = new_calorie_goal = None
    protein_macros = fat_macros = carb_macros = 0
    form = UserDataForm()
    if form.validate_on_submit():
        current_user.age = form.age.data
        current_user.height = form.height.data
        current_user.sex = form.sex.data
        current_user.activity_level = form.activity_level.data
        current_user.current_weight = form.current_weight.data
        current_user.goal_weight = form.goal_weight.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        current_user.age = form.age.data
        current_user.height = form.height.data
        current_user.sex = form.sex.data
        current_user.activity_level = form.activity_level.data
        current_user.current_weight = form.current_weight.data
        current_user.goal_weight = form.goal_weight.data
    return render_template('info.html', title='Info',
                         form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                         form=form)