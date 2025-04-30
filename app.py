from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from data_models import db, Author, Book
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'

db.init_app(app)
@app.route("/author/<int:id>")
def author_detail(id):
    author = Author.query.get_or_404(id)
    return render_template("author_detail.html", author=author)


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
        #return redirect(url_for("author_detail", id=author_id))
    return render_template("add_author.html")

with app.app_context():
    db.create_all()

app.run(port=5002, debug=True)