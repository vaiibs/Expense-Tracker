from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  #db configuration
db = SQLAlchemy(app)

class Expense(db.Model):  # Created Database Model
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(500))                     

with app.app_context():  # Initialize db
    db.create_all()                   

@app.route('/')
def home():
    expenses = Expense.query.all() 
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        comments = request.form['comments']
        new_expense = Expense(category=category, amount=amount, comments=comments)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_expense.html')

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.category = request.form['category']
        expense.amount = request.form['amount']
        expense.comments = request.form['comments']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
