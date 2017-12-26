from models import *

db.drop_all()
db.create_all()

user = Reader(username='Admin', password='sha256$QAZsbOCF$eda7c21fd3f65ff9ba\
								7125a0cb2ba37ab5a7f6f8ab87d9c6e9da2c5211346720')
db.session.add(user)

books = [u"Идиот", u"Анна Каренина", u"Мастер и Маргарита", u"100 лет одиночества", u"Колыбель для кошки",
			u"Прощай оружие", u"Повелитель мух", u"Чапаев и пустота", u"Бойцовский клуб", u"451 градус по Фаренгейту"]

authors = [u"Федор Достоевский", u"Лев Толстой", u"Михаил Булгаков", u"Габриэль Гарсия Маркес", u"Курт Воннегут",
			u"Эрнест Хемингуэй",u"Уильям Голдинг", u"Виктор Пелевин", u"Чак Паланик", u"Рэй Дуглас Брэдбери"]


for i in range(len(authors)):
	
	book = Book(book_name=books[i])
	db.session.add(book)
	
	author = Author(author_name=authors[i])
	db.session.add(author)

	author.writers.append(book)

db.session.commit()
