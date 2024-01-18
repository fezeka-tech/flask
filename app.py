
# app.py

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home/fezekan/mysite/app.py.db'
db = SQLAlchemy(app)

# Define a simple model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))


# Create tables in the database
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name
        })
    return jsonify({'books': book_list})

@app.route('/api/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    author_list = []
    for author in authors:
        author_list.append({
            'id': author.id,
            'name': author.name
        })
    return jsonify({'authors': author_list})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data['title']
    book.author = data['author']

    db.session.commit()

    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})



if __name__ == '__main__':
    app.run(host='0.0.0.0')



