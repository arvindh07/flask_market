from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import Registration, LoginForm
from market import db
from flask_login import login_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route("/register", methods=["GET", "POST"])
def registration_page():
    form = Registration()
    if form.validate_on_submit():
        # print(f'dta {form.data}')
        user_to_create = User(username=form.username.data,
                            password=form.password.data,
                            email=form.email.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Error: {err}', category="danger")
    return render_template("registration.html", form=form)

@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # check 2 things:
        # whether user exists and password is matching with our db
        trying_user = User.query.filter_by(username=form.username.data).first()
        if trying_user and trying_user.check_password(entered_password=form.password.data):
            login_user(trying_user)
            flash(f'Successfully logged in as {trying_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Invalid credentials! Please try again', category='danger')
    return render_template('login.html', form=form)