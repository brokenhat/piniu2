from flask_wtf import FlaskForm, RecaptchaField
from app import app

from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextAreaField, SubmitField, DateField

from flask_ckeditor import CKEditorField

from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Nazwa Użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Użyj innej nazwy użytkownika.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Użyj innego adresu email.')


# zmiana nazwy użytkownika
class EditProfileForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    submit = SubmitField('Zmień')


# publikacja postów
class PostForm(FlaskForm):
    post = CKEditorField('Stwórz nowego posta', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


# edycja postów
class UpdatePost(FlaskForm):
    post = CKEditorField('Edycja posta', validators=[
        DataRequired()])
    update = SubmitField('Dokonaj zmian')


class DeletePost(FlaskForm):
    delete = SubmitField('Usuń')


class NewPage(FlaskForm):
    title = StringField('Tytuł strony', validators=[DataRequired("Dodaj nazwę strony")])
    submit = SubmitField('Dodaj')


class RemovePage(FlaskForm):
    remove = SubmitField('Usuń stronę')


class IsIndex(FlaskForm):
    question = SubmitField('Ustaw')


class UploadFile(FlaskForm):
    image = FileField('Dodawanie obrazka.',
                      validators=[FileRequired("Wybierz obrazek z urządzenia")])
    descr = TextAreaField('Opis obrazka')
    add = SubmitField('Prześlij')


class UploadAttach(FlaskForm):
    attach = FileField('Dodawanie załącznika', validators=[FileRequired()])
    descr = TextAreaField('Dodaj opis linku. (opcjonalnie)')
    add = SubmitField('Prześlij')


class AddContactForm(FlaskForm):
    insert = SubmitField("Wstaw formularz kontaktowy.")


class ContactForm(FlaskForm):
    name = StringField("Imię", validators=[DataRequired("Wprowadź imię")])
    email = StringField("Email", validators=[DataRequired("Wprowadź Email"), Email()])
    subject = StringField('Temat', validators=[DataRequired()])
    message = TextAreaField('Wiadomość', validators=[DataRequired("Wprowadź wiadomość")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Wyślij")


class DateForm(FlaskForm):
    dt = DateField("Wybierz datę", format="%d.%m.%Y")
    submit = SubmitField("Ustaw przypomnienie")
