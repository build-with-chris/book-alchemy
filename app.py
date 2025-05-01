from flask import Flask, request, render_template, jsonify
from data_models import db, Author, Book
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'

db.init_app(app)
@app.route("/home")
def home():
    sort_by= request.args.get('sort_by', 'title')
    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()
    return render_template("home.html", books=books, sort_by=sort_by)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        author = Author(
            name=request.form['name'],
            birth_date=request.form['birthdate'],
            death_date=request.form['date_of_death']
        )
        db.session.add(author)
        db.session.commit()
        return f'Successfully added this author'
    return render_template("add_author.html")


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = Book(
            isbn =request.form['isbn'],
            title=request.form['title'],
            publication_year=request.form['publication_year'],
            author_id=request.form['author_id'],
            book_cover=f"https://covers.openlibrary.org/b/isbn/{request.form['isbn']}-M.jpg"
        )
        db.session.add(book)
        db.session.commit()
        return f"Successfully saved {book.title}."
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


# with app.app_context():
#   db.create_all()
app.run(port=5002, debug=True)