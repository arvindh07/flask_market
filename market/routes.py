from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import Registration, LoginForm, PurchaseItem, SellItem
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItem()
    sell_form = SellItem()
    if request.method == "POST":
        p_item = Item.query.filter_by(name=request.form.get('purchased_item')).first()
        s_item = Item.query.filter_by(name=request.form.get('sold_item')).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash(f'Congratulations! You have purchased {p_item.name}', category="success")
            else:
                flash(f'Unfortunately! You dont have budget to buy {p_item.name}', category="danger")
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash(f'Congratulations! You have sold {s_item.name}', category="success")
            else:
                flash(f'Something went wrong!', category="danger")
        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        purchased_item = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", 
                               items=items, 
                               purchase_form=purchase_form,
                               purchased_item=purchased_item,
                               sell_form=sell_form)

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
        login_user(user_to_create)
        flash(f'Account created successfully! Logged in as {user_to_create.username}', category="info")
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

@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'Logged out successfully', category="info")
    return redirect(url_for("home_page"))