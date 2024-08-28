from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskWeb import db, bcrypt
from flaskWeb.forms import RegistrationForm, LoginForm, UpdateAccountForm, UserDataForm, FoodForm
from flaskWeb.models import User, Food
from flask_login import login_user, current_user, logout_user, login_required
from flaskWeb.DataVisualization import calculate_bmr, calculate_calorie_needs, calculate_macros_protein, calculate_macros_carbs, calculate_macros_fat, calculate_weight_loss_plan, get_nutritional_data

main = Blueprint('main', __name__)

# API keys 
app_id = "9eaa615e"  # Edamam app ID
app_key = "823633324aefbe4dd49f24180783c007"  #Edamam app key

@main.route("/", methods=['GET', 'POST'])
def root():
    return redirect(url_for('login'))

@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    user_data = User.query.filter_by(id=current_user.id).all()
    form = FoodForm()
    if form.validate_on_submit():
        food_data = get_nutritional_data(form.name.data, form.serving_size.data, app_id, app_key)
        if food_data is not None:
            calories = food_data.get("calories", 0)
            protein = food_data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0)
            fat = food_data.get("totalNutrients", {}).get('FAT', {}).get('quantity', 0)
            carbs = food_data.get("totalNutrients", {}).get('CHOCDF', {}).get('quantity', 0)

            food = Food(
                name=form.name.data,
                serving_size=form.serving_size.data,
                calories=calories,
                protein=protein,
                fat=fat,
                carbs=carbs,
                user_id=current_user.id
            )
            db.session.add(food)
            db.session.commit()
            flash('Food item added successfully!', 'success')
        else:
            flash('Failed to fetch food data. Please check your input and try again.', 'danger')
    return render_template("index.html", title="Home", values=user_data, form=form)

@main.route("/view")
def view():
    users = User.query.all()
    return render_template("view.html", values=users)

@main.route("/info", methods=['GET', 'POST'])
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
    elif request.method == 'GET':
        form.age.data = current_user.age
        form.height.data = current_user.height
        form.sex.data = current_user.sex
        form.activity_level.data = current_user.activity_level
        form.current_weight.data = current_user.current_weight
        form.goal_weight.data = current_user.goal_weight
    bmr = calculate_bmr(current_user.sex, current_user.current_weight, current_user.height, current_user.age)
    tdee = calculate_calorie_needs(current_user.activity_level, bmr)
    protein_macros = calculate_macros_protein(current_user.current_weight)
    fat_macros = calculate_macros_fat(current_user.current_weight)
    carb_macros = calculate_macros_carbs(tdee, protein_macros, fat_macros)
    weeks_to_goal, new_calorie_goal = calculate_weight_loss_plan(current_user.current_weight, current_user.goal_weight)
    return render_template('info.html', title='User Info', form=form, tdee=tdee, protein_macros=protein_macros, fat_macros=fat_macros, carb_macros=carb_macros, new_calorie_goal=new_calorie_goal, weeks_to_goal=weeks_to_goal)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
@main.route("/logout")
def logout():    
    logout_user()
    return redirect(url_for('home'))

@main.route("/account", methods=['GET', 'POST'])
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
    return render_template('account.html', title='Account', form=form)
