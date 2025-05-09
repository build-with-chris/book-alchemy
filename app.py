from crypt import methods

from flask import Flask, request, render_template, jsonify, url_for, flash, get_flashed_messages
from data_models import db, Author, Book
from sqlalchemy import or_
from werkzeug.utils import redirect
import os
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"



app.secret_key = "1234"

db.init_app(app)

@app.route("/")
def redirect_home():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    sort_by= request.args.get('sort_by', 'title')
    search = request.args.get('search')
    query = Book.query.join(Author)

    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()

    if search:
        books = query.filter(db.or_(Book.title.ilike(f"%{search}%"),
                                    Author.name.ilike(f"%{search}%"))).all()
    return render_template("home.html", books=books, sort_by=sort_by, search=search)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        author = Author(
            name=request.form['name'],
            birth_date=request.form['birthdate'],
            death_date=request.form['date_of_death']
        )
        try:
            db.session.add(author)
            db.session.commit()
            flash(f'Successfully added this author')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash("This author name is already in the database.")
            return redirect(url_for('home'))

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
        flash(f"Successfully saved {book.title}.")
        return redirect(url_for('home'))
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
    book_to_delete = Book.query.get_or_404(book_id)
    author=book_to_delete.author
    db.session.delete(book_to_delete)
    db.session.commit()
    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f'Book {book_to_delete.title} AND {author.name} were successfully deleted.')
    else:
        flash(f'Book {book_to_delete.title} was successfully deleted.')
    return redirect(url_for('home'))


@app.route("/book/<int:book_id>/update", methods=["GET", "POST"])
def update_book(book_id):
    book = Book.query.get(book_id)
    authors= Author.query.order_by(Author.name).all()
    if request.method == "POST":
        book.isbn = request.form["isbn"]
        book.title =  request.form["title"]
        book.publication_year = request.form["year"]
        book.author_id = request.form["author_id"]

        db.session.commit()
        flash("book is updated.")
        return redirect(url_for('home'))
    return render_template('update.html', book=book, authors=authors)



with app.app_context():
    db.create_all()
app.run(port=5002, debug=True)