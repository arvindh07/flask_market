from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    hash_password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_by', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, password_to_hash):
        self.hash_password = bcrypt.generate_password_hash(password_to_hash).decode('utf-8')

    def check_password(self, entered_password):
        return bcrypt.check_password_hash(self.hash_password, entered_password)

    def can_purchase(self, p_item):
        return self.budget >= p_item.price
    
    def can_sell(self, s_item):
        return s_item in self.items
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False, unique=False)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'
    
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()