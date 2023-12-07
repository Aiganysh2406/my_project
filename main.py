from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre = db.Column(db.String)
    created_at = db.Column(db.Date)

db.create_all()

class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    created_item: str  


def create_book():
    data = request.get_json()
    book_data = BookSchema(**data)
    new_book = Book(**book_data.model_dict())
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'})


def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'created_at': str(book.created_item)} for book in books]
    return jsonify({'books': book_list})


def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'created_at': str(book.created_item)})
    else:
        return jsonify({'message': 'Book not found'})


def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        book_data = BookSchema(**data)
        book.title = book_data.title
        book.author = book_data.author
        book.genre = book_data.genre
        book.created_item = book_data
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'message': 'Book not found'})

def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'message': 'Book not found'})

if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

             