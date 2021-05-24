from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from models import *
from importlib import reload
from datetime import timedelta
import forms


@app.before_request
def before_request():
	# перезагрузка форм 
	# AuthorBooksForm
	# ReaderSigninForm 
	reload(forms)


@app.before_request
def make_session_permanent():
	'''сброс неактивной сессии'''
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=40)


def redirect_url(default='books'):
	'''редирект на последнюю страницу'''
	return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@login_manager.user_loader
def load_user(user_id):
	return Reader.query.get(int(user_id))


@app.route('/sign_in', methods=['POST'])
def sign_in():
	""" логин """
	reader_signin_form = forms.ReaderSigninForm()
	user = Reader.query.filter_by(username=reader_signin_form.readers.data).first()
	# логин
	login_user(user)
	flash('Вы вошли в систему', category="text-success")
	return redirect(redirect_url('books'))


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
	""" регистрация """
	reader_signin_form = forms.ReaderSigninForm()
	reader_signup_form = forms.ReaderRegisterForm()

	# проверка правильности заполнения формы
	if reader_signup_form.validate_on_submit():
		# проверка username на уникальность
		username = Reader.query.filter_by(username=reader_signup_form.username.data).first()
		if not username:
			# проверка двух password-полей
			if reader_signup_form.password.data == reader_signup_form.confirm_password.data:
				# хеширование пароля и добавление нового пользователя
				hashed_password = generate_password_hash(reader_signup_form.password.data, method='sha256')
				new_user = Reader(username=reader_signup_form.username.data,password=hashed_password)
				db.session.add(new_user)
				db.session.commit()
				
				flash('Пользователь успешно создан', category="text-success")
				return redirect(url_for('books'))

			flash('Пароли не совпадают', category="text-danger")
			return render_template('sign_up.html', reader_signin_form=reader_signin_form,
		                                           reader_signup_form=reader_signup_form)

		flash('Такое имя уже существует', category="text-danger")
		return render_template('sign_up.html', reader_signin_form=reader_signin_form,
		                                       reader_signup_form=reader_signup_form)

	return render_template('sign_up.html', reader_signin_form=reader_signin_form,
	                                       reader_signup_form=reader_signup_form)

@login_required
@app.route('/logout')
def logout():
	logout_user()
	flash('Вы вышли из системы', category="text-success")
	return redirect(redirect_url())

#----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def books():
	""" список книг """
	reader_signin_form = forms.ReaderSigninForm()
	search_form = forms.SearchForm()
	books = Book.query.all()
	book_name_form = forms.BookNameForm()

	return render_template('books.html', reader_signin_form=reader_signin_form,
	                                     search_form=search_form,
										 books=books,
										 book_name_form=book_name_form)


@app.route('/add_book', methods=['POST'])
def add_book():
	""" добавить книгу """
	book_name_form = forms.BookNameForm()
	
	# наличие заполненной формы
	if book_name_form.name.data:
		# проверка имени на уникальность
		book_name = Book.query.filter_by(book_name=book_name_form.name.data).first()
		if not book_name:
			# создание новой книги
			new_book = Book(book_name=book_name_form.name.data)
			db.session.add(new_book)
			db.session.commit()

			flash('Успех', category="text-success")
			return redirect(url_for('books'))

		flash('Такая книга уже существует', category="text-danger")
		return redirect(url_for('books'))

	flash('Введите название', category="text-danger")
	return redirect(url_for('books'))


@app.route('/edit_book/<int:book_id>',methods=['POST'])
def edit_book(book_id):
	""" изменить название книги """
	book_name_form = forms.BookNameForm()
	book = Book.query.filter_by(book_id=book_id).first()

	# наличие заполненной формы
	if book_name_form.name.data:
		# проверка имени на уникальность
		new_book_name = Book.query.filter_by(book_name=book_name_form.name.data).first()
		if not new_book_name:
			# изменение имени книги
			book.book_name = book_name_form.name.data
			db.session.commit()

			flash('Успех', category="text-success")
			return redirect(redirect_url())

		flash('Такая книга уже существует или введённое название идентично старому', 
			category="text-danger")
		return redirect(redirect_url())

	flash('Введите новое название', category="text-danger")
	return redirect(redirect_url())


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
	""" удалить книгу """
	book = Book.query.filter_by(book_id=book_id).first()
	db.session.delete(book)
	db.session.commit()

	flash('Успех', category="text-success")
	return redirect(url_for('books'))

#----------------------------------------------------------------------------------------------------------------------

@app.route('/authors')
def authors():
	""" список авторов """
	reader_signin_form = forms.ReaderSigninForm()
	search_form = forms.SearchForm()
	authors = Author.query.all()
	author_name_form = forms.AuthorNameForm()
	author_book_form = forms.AuthorBooksForm()
	return render_template('authors.html', reader_signin_form=reader_signin_form,
											search_form=search_form,
											authors=authors,
											author_name_form=author_name_form,
											author_book_form=author_book_form)


@app.route('/add_author', methods=['POST'])
def add_author():
	""" добавить автора """
	author_name_form = forms.AuthorNameForm()

	# наличие заполненной формы
	if author_name_form.name.data:
		# проверка имени на уникальность
		author_name = Author.query.filter_by(
			author_name=author_name_form.name.data).first()
		if not author_name:
			# создание нового автора
			new_author = Author(author_name=author_name_form.name.data)
			db.session.add(new_author)
			db.session.commit()

			flash('Успех', category="text-success")
			return redirect(url_for('authors'))
		
		flash('Такой автор уже существует', category="text-danger")
		return redirect(url_for('authors'))

	flash('Введите новое имя', category="text-danger")
	return redirect(url_for('authors'))


@app.route('/edit_author/<int:author_id>', methods=['POST'])
def edit_author(author_id):
	""" изменить имя автора """
	author_name_form = forms.AuthorNameForm()
	author = Author.query.filter_by(author_id=author_id).first()
	
	# наличие заполненной формы
	if author_name_form.name.data:
		# проверка имени на уникальность
		new_author_name = Author.query.filter_by(
			author_name=author_name_form.name.data).first()
		if not new_author_name:
			# изменение имени автора
			author.author_name = author_name_form.name.data
			db.session.commit()

			flash('Успех', category="text-success")
			return redirect(redirect_url())

		flash('Такой автор уже существует или введённое имя идентично старому', 
			category="text-danger")
		return redirect(redirect_url())

	flash('Введите новое имя', category="text-danger")
	return redirect(redirect_url())


@app.route('/add_books_to_author/<int:author_id>', methods=['POST'])
def add_books_to_author(author_id):
	""" изменить список книг """
	books = Book.query.all()

	author = Author.query.filter_by(author_id=author_id).first()
	author_book_form = forms.AuthorBooksForm()

	book_list = []
	for book in author_book_form.books.data:
		book = Book.query.filter_by(book_name=book).first()
		book_list.append(book)
	
	author.writers = book_list
	db.session.commit()

	flash('Успех', category="text-success")
	return redirect(redirect_url())


@app.route('/delete_author/<int:author_id>')
def delete_author(author_id):
	""" удалить автора """
	author = Author.query.filter_by(author_id=author_id).first()
	db.session.delete(author)
	db.session.commit()

	flash('Успех', category="text-success")
	return redirect(url_for('authors'))

#----------------------------------------------------------------------------------------------------------------------

@app.route('/search_book', methods=['POST'])
def search_book():
	""" поиск книг """
	search_form = forms.SearchForm()

	if search_form.name.data:

		book = Book.query.filter_by(book_name=search_form.name.data).first()
		if book:
			flash('Успех', category="text-success")
			return redirect(url_for('search_result_book', id=book.book_id))
		else:
			flash('Книга не найдена', category="text-danger")
			return redirect(redirect_url())
		
	return redirect(redirect_url())


@app.route('/search_author', methods=['POST'])
def search_author():
	""" поиск книг """
	search_form = forms.SearchForm()

	if search_form.name.data:
		
		author = Author.query.filter_by(author_name=search_form.name.data).first()
		if author:
			flash('Успех', category="text-success")
			return redirect(url_for('search_result_author', id=author.author_id))
		else:
			flash('Автор не найден', category="text-danger")
			return redirect(redirect_url())
		
	return redirect(redirect_url())


@app.route('/search_result_book/<int:id>')
def search_result_book(id):
	""" результат поиска книг"""
	reader_signin_form = forms.ReaderSigninForm()
	search_form = forms.SearchForm()
	book_name_form = forms.BookNameForm()
	book = Book.query.filter_by(book_id=id).first()
	return render_template('search_result.html', reader_signin_form=reader_signin_form,
													search_form=search_form,
													book=book,
													book_name_form=book_name_form)


@app.route('/search_result_author/<int:id>')
def search_result_author(id):
	""" результат поиска авторов"""
	reader_signin_form = forms.ReaderSigninForm()
	search_form = forms.SearchForm()
	author_name_form = forms.AuthorNameForm()
	author_book_form = forms.AuthorBooksForm()
	author = Author.query.filter_by(author_id=id).first()
	return render_template('search_result.html', reader_signin_form=reader_signin_form,
													search_form=search_form,
													author=author,
													author_name_form=author_name_form,
													author_book_form=author_book_form)