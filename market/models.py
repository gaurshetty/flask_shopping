from market import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    image = db.Column(db.String(150), nullable=False, default='profile.jpg')
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def pretty_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{self.budget:,}$'
        else:
            return f'{self.budget}$'


    @property
    def hash_password(self):
        return self.hash_password

    @hash_password.setter
    def hash_password(self, pain_password):
        self.password = bcrypt.generate_password_hash(pain_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def can_purchase(self, p_item_obj):
        return self.budget >= p_item_obj.price

    def can_sell(self, p_item_obj):
        return p_item_obj in self.items

    def cart_count(self):
        return len(self.items)


class Item(db.Model):
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    image = db.Column(db.String(150), nullable=False, default='image.jpg')
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

