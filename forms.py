from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Length
from models import Reader, Book

readers_list = Reader.query.all()
book_list = Book.query.all()

# форма регистрации пользователя
class ReaderRegisterForm(FlaskForm):
	username = StringField('Введите имя', validators=[InputRequired('Введите имя'),
							Length(min=4, max=20, message='размер должен быть между 4 и 20 символами')])
	
	password = PasswordField('Введите пароль', validators=[InputRequired('Введите пароль'),
								Length(min=4, max=20, message='размер должен быть между 4 и 20 символами')])
	
	confirm_password = PasswordField('Подтвердите пароль', validators=[InputRequired('Подтвердите пароль'),
										Length(min=4, max=20, message='размер должен быть между 4 и 20 символами')])

# форма входа пользователя
class ReaderSigninForm(FlaskForm):
	readers = SelectField(choices=[(reader.username, reader.username) for reader in readers_list])

# форма названия книги
class BookNameForm(FlaskForm):
	name = StringField('Введите название книги')

# форма имени автора
class AuthorNameForm(FlaskForm):
	name = StringField('Введите имя автора')

# форма выбора книг автора
class AuthorBooksForm(FlaskForm):
	books = SelectMultipleField(choices=[(book.book_name, book.book_name) for book in book_list])

# форма поиска
class SearchForm(FlaskForm):
	name = StringField('Поиск')