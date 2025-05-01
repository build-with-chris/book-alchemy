from crypt import methods

from flask import Flask, request, render_template, jsonify, url_for, flash, get_flashed_messages
from data_models import db, Author, Book
from sqlalchemy import or_
from werkzeug.utils import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
app.secret_key = "1234"

db.init_app(app)
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
        db.session.add(author)
        db.session.commit()
        flash(f'Successfully added this author')
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
    db.session.delete(book_to_delete)
    db.session.commit()
    flash(f'Book {book_to_delete.title} was successfully deleted.')
    return redirect(url_for('home'))


# with app.app_context():
#   db.create_all()
app.run(port=5002, debug=True)