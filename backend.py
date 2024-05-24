from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    transaction = Transaction(user_id=data['user_id'], amount=data['amount'], date=datetime.strptime(data['date'], '%Y-%m-%d'), category=data['category'])
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added"}), 201

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_id = data['user_id']
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Prepare data for predictive model
    df = pd.DataFrame([(t.amount, t.date) for t in transactions], columns=['amount', 'date'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['month'] = df.index.month
    df['year'] = df.index.year

    # Simple predictive model
    X = df[['month', 'year']]
    y = df['amount']
    model = LinearRegression()
    model.fit(X, y)

    # Predict next month's expenses
    next_month = pd.to_datetime('today') + pd.DateOffset(months=1)
    prediction = model.predict([[next_month.month, next_month.year]])

    return jsonify({"predicted_expense": prediction[0]})

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
