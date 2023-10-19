from app import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    year = db.Column(db.String)
    #books = db.relationship("Book", backref="author")

    def __repr__(self):
        return '<student: {}>'.format(self.name)

'''
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    title = db.Column(db.String)
    '''