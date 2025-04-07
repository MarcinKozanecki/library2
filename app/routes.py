from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import Book, Author, Borrowing
from datetime import datetime

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            author = Author(name=name)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        selected_authors = request.form.getlist('authors')
        if title and selected_authors:
            book = Book(title=title)
            for author_id in selected_authors:
                author = Author.query.get(author_id)
                book.authors.append(author)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_book.html', authors=authors)

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.is_available:
        borrower_name = request.form['borrower']
        borrowing = Borrowing(
            borrower_name=borrower_name,
            date_borrowed=datetime.now(),
            book=book
        )
        book.is_available = False
        db.session.add(borrowing)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    borrowing = Borrowing.query.filter_by(book_id=book_id, date_returned=None).first()
    if borrowing:
        borrowing.date_returned = datetime.now()
        book.is_available = True
        db.session.commit()
    return redirect(url_for('index'))
