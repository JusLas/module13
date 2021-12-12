from app import db
from marshmallow import Schema, fields

books_authors = db.Table('books_authors',
    db.Column(
        'book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column(
        'author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    publication_year = db.Column(db.Integer, index=True)
    read = db.Column(db.Boolean, default=False)
    authors = db.relationship(
        'Author', secondary=books_authors, lazy='subquery',
        backref=db.backref('books', lazy=True))
    events = db.relationship("BookEvents", backref="book", lazy="dynamic")
    
    def __str__(self):
        return f"<Book {self.title}>"


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    publication_year = fields.Int()
    read = fields.Bool()
    events = fields.Nested(lambda: BookEventsSchema, many=True)


class BookWithAuthorsSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    publication_year = fields.Int()
    read = fields.Bool()
    authors = fields.Nested(lambda: AuthorSchema, many=True)
    events = fields.Nested(lambda: BookEventsSchema, many=True)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), index=True)
    last_name = db.Column(db.String(200), index=True)

    def __str__(self):
        return f"<Author {self.first_name} {self.last_name}>"


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()

class AuthorWithBooksSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    books = fields.Nested(lambda: BookSchema, many=True)


class BookEvents(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   lent = db.Column(db.DateTime, index=True)
   returned = db.Column(db.DateTime, index=True)
   book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

   def __str__(self):
        return f"<Book event {self.id}>"

class BookEventsSchema(Schema):
    id = fields.Int(dump_only=True)
    lent = fields.DateTime()
    returned = fields.DateTime()


book_schema = BookSchema()
book_with_authors_schema = BookWithAuthorsSchema()
author_schema = AuthorSchema()
author_with_books_schema = AuthorWithBooksSchema()
