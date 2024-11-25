from flask import Blueprint, render_template, request, redirect, url_for
from website import db
from website.models import Book

user = Blueprint('user', __name__)

# Route for the home page (Book list page for users)
@user.route('/')
def user_home():
    # Query all books to show to the user
    books = Book.query.all()
    return render_template('user_home.html', books=books)

# Route to download a book (PDF)
@user.route('/download_book/<int:book_id>')
def download_book(book_id):
    # Find the book by its ID
    book = Book.query.get_or_404(book_id)
    return redirect(url_for('static', filename=book.file_path))
