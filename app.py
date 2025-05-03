import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

# ------------------------------
# Point Flask at your sub-folder
# ------------------------------
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT  = os.path.join(BASE_DIR, 'library-app')

app = Flask(
    __name__,
    static_folder=os.path.join(PROJECT_ROOT, 'static'),
    template_folder=os.path.join(PROJECT_ROOT, 'templates')
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secretkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------------------
# Models
# ------------------------------
class Book(db.Model):
    id             = db.Column(db.Integer,   primary_key=True)
    book_id        = db.Column(db.String(20), unique=True, nullable=False)
    title          = db.Column(db.String(120), nullable=False)
    author         = db.Column(db.String(80),  nullable=False)
    genre          = db.Column(db.String(50))
    year           = db.Column(db.String(4))
    available      = db.Column(db.Boolean,     default=True)
    times_borrowed = db.Column(db.Integer,     default=0)

class Member(db.Model):
    id         = db.Column(db.Integer,   primary_key=True)
    member_id  = db.Column(db.String(20), unique=True, nullable=False)
    name       = db.Column(db.String(80),  nullable=False)
    contact    = db.Column(db.String(120))

class Borrow(db.Model):
    id          = db.Column(db.Integer,       primary_key=True)
    book_id     = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id   = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.Date,          default=date.today)
    return_date = db.Column(db.Date,          nullable=True)
    late_fee    = db.Column(db.Integer,       default=0)

    book   = db.relationship('Book',   backref='borrows')
    member = db.relationship('Member', backref='borrows')

# ------------------------------
# Book Routes
# ------------------------------
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_id = request.form['book_id'].strip()
        title   = request.form['title'].strip()
        author  = request.form['author'].strip()
        genre   = request.form['genre'].strip()
        year    = request.form['year'].strip()

        if Book.query.filter_by(book_id=book_id).first():
            return render_template('add_book.html',
                                   error="Book ID already exists.",
                                   form=request.form)

        new_book = Book(
            book_id=book_id,
            title=title,
            author=author,
            genre=genre,
            year=year
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Added "{title}" successfully!')
        return redirect(url_for('index'))

    return render_template('add_book.html', form={})

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.book_id = request.form['book_id'].strip()
        book.title   = request.form['title'].strip()
        book.author  = request.form['author'].strip()
        book.genre   = request.form['genre'].strip()
        book.year    = request.form['year'].strip()
        db.session.commit()
        flash(f'Updated "{book.title}" successfully!')
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f'Deleted "{title}" successfully!')
    return redirect(url_for('index'))

# ------------------------------
# Member Routes
# ------------------------------
@app.route('/members')
def list_members():
    members = Member.query.all()
    return render_template('members.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        mem_id  = request.form['member_id'].strip()
        name    = request.form['name'].strip()
        contact = request.form['contact'].strip()

        if Member.query.filter_by(member_id=mem_id).first():
            return render_template('add_member.html',
                                   error="Member ID already exists.",
                                   form=request.form)

        m = Member(member_id=mem_id, name=name, contact=contact)
        db.session.add(m)
        db.session.commit()
        flash(f'Added member "{name}" successfully!')
        return redirect(url_for('list_members'))

    return render_template('add_member.html', form={})

@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    m = Member.query.get_or_404(id)
    if request.method == 'POST':
        m.member_id = request.form['member_id'].strip()
        m.name      = request.form['name'].strip()
        m.contact   = request.form['contact'].strip()
        db.session.commit()
        flash(f'Updated member "{m.name}" successfully!')
        return redirect(url_for('list_members'))
    return render_template('edit_member.html', member=m)

@app.route('/members/delete/<int:id>', methods=['POST'])
def delete_member(id):
    m = Member.query.get_or_404(id)
    name = m.name
    db.session.delete(m)
    db.session.commit()
    flash(f'Deleted member "{name}" successfully!')
    return redirect(url_for('list_members'))

# ----- Borrow & Return -----
@app.route('/borrows')
def list_borrows():
    active = Borrow.query.filter_by(return_date=None).all()
    return render_template('borrows.html', borrows=active)

@app.route('/borrow', methods=['GET','POST'])
def borrow_book():
    if request.method == 'POST':
        book_id   = int(request.form['book_id'])
        member_id = int(request.form['member_id'])

        book   = Book.query.get_or_404(book_id)
        member = Member.query.get_or_404(member_id)
        book.available = False
        book.times_borrowed += 1

        b = Borrow(book_id=book_id, member_id=member_id)
        db.session.add_all([book, b])
        db.session.commit()
        flash(f'Checked out "{book.title}" to {member.name}.')
        return redirect(url_for('list_borrows'))

    books   = Book.query.filter_by(available=True).all()
    members = Member.query.all()
    return render_template('borrow.html', books=books, members=members)

@app.route('/return/<int:id>', methods=['POST'])
def return_book(id):
    b = Borrow.query.get_or_404(id)
    b.return_date = date.today()
    days = (b.return_date - b.borrow_date).days
    b.late_fee = max(0, days - 14)
    book = Book.query.get_or_404(b.book_id)
    book.available = True

    db.session.commit()
    flash(f'"{book.title}" returned; late fee = ${b.late_fee}.')
    return redirect(url_for('list_borrows'))

# ------------------------------
# Inject current time into templates
# ------------------------------
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# ------------------------------
# Run
# ------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=3000)
