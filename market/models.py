from market import db
from market import bcrypt

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    hash_password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    items = db.relationship('Item', backref='owned_by', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, password_to_hash):
        self.hash_password = bcrypt.generate_password_hash(password_to_hash).decode('utf-8')

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False, unique=False)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'