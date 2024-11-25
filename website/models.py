from . import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each book
    title = db.Column(db.String(255), nullable=False)  # Title of the book
    author = db.Column(db.String(255), nullable=False)  # Author of the book
    publication_year = db.Column(db.Integer, nullable=True)  # Year of publication
    short_description = db.Column(db.Text, nullable=True)  # Short description of the book
    file_path = db.Column(db.String(255), nullable=False)  # Path to the uploaded book file

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
