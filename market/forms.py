from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from market.models import User


class RegistrationForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists, try another username!")
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email already in use, try to login with this email!")

    username = StringField(label='User Name:', validators=[Length(min=4,max=30),DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Set Password:', validators=[Length(min=4,max=30),DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', 'Password does not match!'),DataRequired()])
    image = FileField(label='Image:', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'], 'Images only!')])
    submit = SubmitField(label='Create Account')


class UserForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=4,max=30),DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(),DataRequired()])
    budget = IntegerField(label='Budget:')
    image = FileField(label='Image:', validators=[FileAllowed(['jpg','jpeg','png','gif'], 'Images only!')])
    submit = SubmitField(label='Update user')


class ItemForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    barcode = StringField(label='Barcode:', validators=[DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    image = FileField(label='Image:', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'], 'Images only!')])
    submit = SubmitField(label='Add Item')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Buy')


class SellForm(FlaskForm):
    submit = SubmitField(label='Sell Item')


class DeleteForm(FlaskForm):
    submit = SubmitField(label='Delete')

