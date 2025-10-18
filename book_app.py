from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

books = []
borrowers = []
loans = []

book_id_counter = 1
borrower_id_counter = 1
loan_id_counter = 1

# BOOKS CRUD 
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/api/books', methods=['POST'])
def add_book():
    global book_id_counter
    data = request.json
    book = {
        'id': book_id_counter,
        'title': data['title'],
        'author': data['author']
    }
    books.append(book)
    book_id_counter += 1
    return jsonify(book), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def edit_book(book_id):
    data = request.json
    for book in books:
        if book['id'] == book_id:
            book['title'] = data['title']
            book['author'] = data['author']
            book['genre'] = data.get('genre', '')
            book['isbn'] = data.get('isbn', '')
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return '', 204

# BORROWERS CRUD
@app.route('/api/borrowers', methods=['GET'])
def get_borrowers():
    return jsonify(borrowers)

@app.route('/api/borrowers', methods=['POST'])
def add_borrower():
    global borrower_id_counter
    data = request.json
    borrower = {
        'id': borrower_id_counter,
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone']
    }
    borrowers.append(borrower)
    borrower_id_counter += 1
    return jsonify(borrower), 201

@app.route('/api/borrowers/<int:borrower_id>', methods=['PUT'])
def edit_borrower(borrower_id):
    data = request.json
    for borrower in borrowers:
        if borrower['id'] == borrower_id:
            borrower['name'] = data['name']
            borrower['email'] = data['email']
            borrower['phone'] = data['phone']
            return jsonify(borrower)
    return jsonify({'error': 'Borrower not found'}), 404

@app.route('/api/borrowers/<int:borrower_id>', methods=['DELETE'])
def delete_borrower(borrower_id):
    global borrowers
    borrowers = [b for b in borrowers if b['id'] != borrower_id]
    return '', 204

#LOANS CRUD
@app.route('/api/loans', methods=['GET'])
def get_loans():
    return jsonify(loans)

@app.route('/api/loans', methods=['POST'])
def add_loan():
    global loan_id_counter
    data = request.json
    loan = {
        'id': loan_id_counter,
        'book_id': data['book_id'],
        'borrower_id': data['borrower_id'],
        'due_date': data['due_date'],
        'return_date': data.get('return_date', None),
        'status': data.get('status', None)
    }
    loans.append(loan)
    loan_id_counter += 1
    return jsonify(loan), 201

@app.route('/api/loans/<int:loan_id>', methods=['PUT'])
def edit_loan(loan_id):
    data = request.json
    for loan in loans:
        if loan['id'] == loan_id:
            loan['book_id'] = data['book_id']
            loan['borrower_id'] = data['borrower_id']
            loan['due_date'] = data['due_date']
            loan['return_date'] = data.get('return_date', None)
            loan['status'] = data.get('status', loan.get('status', None))
            return jsonify(loan)
    return jsonify({'error': 'Loan not found'}), 404

@app.route('/api/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    global loans
    loans = [l for l in loans if l['id'] != loan_id]
    return '', 204

#SERVE FRONTEND
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/templates-image/<path:filename>')
def templates_image(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)