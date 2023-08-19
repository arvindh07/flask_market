from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User
from market.forms import Registration
from market import db

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
                            hash_password=form.password.data,
                            email=form.email.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            print(f'err {err}')
    return render_template("registration.html", form=form)