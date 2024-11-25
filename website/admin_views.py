import os

from flask import Blueprint, redirect, url_for, render_template, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from website import db
from website.models import Book

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    # Query all books
    books = Book.query.all()

    # Get the total number of books in the library
    total_books = len(books)

    # Get the count of recent books, for now, we're just showing the total books
    recent_books_count = len(books)  # Adjust this to filter recent books if needed

    # Get the last added book based on the ID (or use 'created_at' if you have that field)
    last_added_book = Book.query.order_by(Book.id.desc()).first()

    # Render the template and pass the required variables
    return render_template('library.html',
                           total_books=total_books,
                           recent_books_count=recent_books_count,
                           last_added_book=last_added_book)


@admin.route('/manage', methods=['GET'])
def manage_books():
    books = Book.query.all()  # Fetch all books from the database
    return render_template('manage_books.html', books=books)


# Route for deleting a book
@admin.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin.manage_books'))


# Route for editing a book (form to edit details)
@admin.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.publication_year = request.form['publication_year']
        book.short_description = request.form['short_description']

        # Handle file upload (if a new file is uploaded)
        file = request.files.get('file')
        if file:
            filename = file.filename
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            book.file_path = file_path  # Update the file path in the database

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('admin.manage_books'))

    return render_template('edit_book.html', book=book)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@admin.route('/upload', methods=['GET', 'POST'])
def upload_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        short_description = request.form['short_description']
        file = request.files['file']

        # Check if the file exists and is valid
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save the file in the uploads folder

            # Save book data in the database, storing just the filename
            new_book = Book(
                title=title,
                author=author,
                publication_year=publication_year,
                short_description=short_description,
                file_path=filename  # Store only the filename here, not the full path
            )
            db.session.add(new_book)
            db.session.commit()

            return redirect(url_for('admin.home'))

    return render_template('upload.html')

@admin.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the file from the uploads directory
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)