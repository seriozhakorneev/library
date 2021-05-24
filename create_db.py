from models import *

db.drop_all()
db.create_all()

user = Reader(username='Admin', password='Admin')

db.session.add(user)

books = [u"Идиот", u"Анна Каренина", u"Мастер и Маргарита",
         u"100 лет одиночества", u"Колыбель для кошки", u"Прощай оружие",
		 u"Повелитель мух", u"Чапаев и пустота",
		 u"Бойцовский клуб", u"451 градус по Фаренгейту"]

authors = [u"Федор Достоевский", u"Лев Толстой", u"Михаил Булгаков",
           u"Габриэль Гарсия Маркес", u"Курт Воннегут",
		   u"Эрнест Хемингуэй",u"Уильям Голдинг", u"Виктор Пелевин",
		   u"Чак Паланик", u"Рэй Дуглас Брэдбери"]


for i in range(len(authors)):
	
	book = Book(book_name=books[i])
	db.session.add(book)
	
	author = Author(author_name=authors[i])
	db.session.add(author)

	author.writers.append(book)

db.session.commit()
