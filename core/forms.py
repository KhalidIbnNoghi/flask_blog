from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms import Form, StringField, PasswordField, validators

# Форма регистрации
class RegistrationForm(Form):
    email = StringField('Логин', [validators.Length(min=6, max=35)])
    password = PasswordField('Новый пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать'), validators.Length(min=8, max=15)
    ])
    confirm = PasswordField('Подтверждение пароля')

# Форма авторизации
class login_form(FlaskForm):
    email = StringField('Логин', [validators.Length(min=6, max=35)])
    password = PasswordField('Пароль', [validators.DataRequired(), validators.Length(min=8, max=15)])

# Форма для постов
class PostForm(FlaskForm):
    title = StringField(
        'Заголовок', validators=[DataRequired('Это поле обязательно к заполнению!')])
    content = StringField(
        'Описание', validators=[DataRequired('Это поле обязательно к заполнению!')])
