from market import app
from flask import render_template
from market.models import Item
from market.forms import Registration

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route("/register")
def registration_page():
    form = Registration()
    return render_template("registration.html", form=form)