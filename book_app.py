from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://library-management-syste-583ca-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Firebase references
books_ref = db.reference('books')
borrowers_ref = db.reference('borrowers')
loans_ref = db.reference('loans')

# BOOKS CRUD 
@app.route('/api/books', methods=['GET'])
def get_books():
    books = books_ref.get()
    if books is None:
        return jsonify([])
    return jsonify([{**v, 'id': k} for k, v in books.items()])

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    new_book_ref = books_ref.push({
        'title': data['title'],
        'author': data['author'],
        'genre': data.get('genre', ''),
        'isbn': data.get('isbn', '')
    })
    book_id = new_book_ref.key
    book = {**data, 'id': book_id}
    return jsonify(book), 201

@app.route('/api/books/<book_id>', methods=['PUT'])
def edit_book(book_id):
    data = request.json
    books_ref.child(book_id).update({
        'title': data['title'],
        'author': data['author'],
        'genre': data.get('genre', ''),
        'isbn': data.get('isbn', '')
    })
    return jsonify({**data, 'id': book_id})

@app.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    books_ref.child(book_id).delete()
    return '', 204

# BORROWERS CRUD
@app.route('/api/borrowers', methods=['GET'])
def get_borrowers():
    borrowers = borrowers_ref.get()
    if borrowers is None:
        return jsonify([])
    return jsonify([{**v, 'id': k} for k, v in borrowers.items()])

@app.route('/api/borrowers', methods=['POST'])
def add_borrower():
    data = request.json
    new_borrower_ref = borrowers_ref.push({
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone']
    })
    borrower_id = new_borrower_ref.key
    borrower = {**data, 'id': borrower_id}
    return jsonify(borrower), 201

@app.route('/api/borrowers/<borrower_id>', methods=['PUT'])
def edit_borrower(borrower_id):
    data = request.json
    borrowers_ref.child(borrower_id).update({
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone']
    })
    return jsonify({**data, 'id': borrower_id})

@app.route('/api/borrowers/<borrower_id>', methods=['DELETE'])
def delete_borrower(borrower_id):
    borrowers_ref.child(borrower_id).delete()
    return '', 204

# LOANS CRUD
@app.route('/api/loans', methods=['GET'])
def get_loans():
    loans = loans_ref.get()
    if loans is None:
        return jsonify([])
    return jsonify([{**v, 'id': k} for k, v in loans.items()])

@app.route('/api/loans', methods=['POST'])
def add_loan():
    data = request.json
    new_loan_ref = loans_ref.push({
        'book_id': data['book_id'],
        'borrower_id': data['borrower_id'],
        'due_date': data['due_date'],
        'return_date': data.get('return_date', None),
        'status': data.get('status', 'Active')
    })
    loan_id = new_loan_ref.key
    loan = {**data, 'id': loan_id}
    return jsonify(loan), 201

@app.route('/api/loans/<loan_id>', methods=['PUT'])
def edit_loan(loan_id):
    data = request.json
    loans_ref.child(loan_id).update({
        'book_id': data['book_id'],
        'borrower_id': data['borrower_id'],
        'due_date': data['due_date'],
        'return_date': data.get('return_date', None),
        'status': data.get('status', 'Active')
    })
    return jsonify({**data, 'id': loan_id})

@app.route('/api/loans/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loans_ref.child(loan_id).delete()
    return '', 204

# SERVE FRONTEND
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates-image/<path:filename>')
def templates_image(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)