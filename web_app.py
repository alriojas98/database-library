#!/usr/bin/env python3
"""
Web-based Library Management System
Provides a modern web interface for managing books, members, and transactions
"""

from flask import Flask, render_template_string, request, jsonify
from database_sqlite import DatabaseConnectionSQLite
from datetime import date, timedelta
import json

app = Flask(__name__)

def get_db():
    """Create a new database connection for each request (thread-safe)"""
    return DatabaseConnectionSQLite('library_sqlite.db')

def convert_rows(rows):
    """Convert SQLite Row objects to lists"""
    if not rows:
        return []
    result = []
    for row in rows:
        if hasattr(row, 'keys'):  # SQLite Row object
            result.append(list(row))
        else:
            result.append(row if isinstance(row, list) else list(row))
    return result

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Library Book Records</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            padding: 20px;
            background: #ecf0f1;
            flex-wrap: wrap;
        }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn-add {
            background: #27ae60;
            color: white;
        }
        
        .btn-add:hover {
            background: #229954;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39,174,96,0.4);
        }
        
        .btn-edit {
            background: #3498db;
            color: white;
        }
        
        .btn-edit:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52,152,219,0.4);
        }
        
        .btn-delete {
            background: #e74c3c;
            color: white;
        }
        
        .btn-delete:hover {
            background: #c0392b;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(231,76,60,0.4);
        }
        
        .btn-stats {
            background: #f39c12;
            color: white;
        }
        
        .btn-stats:hover {
            background: #d68910;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(243,156,18,0.4);
        }
        
        .search-box {
            padding: 20px;
            background: #ecf0f1;
            display: flex;
            gap: 10px;
        }
        
        .search-box input {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .search-box button {
            padding: 10px 20px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .table-container {
            padding: 20px;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        th {
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .stat-card p {
            font-size: 32px;
            font-weight: bold;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        .modal-content h2 {
            margin-bottom: 20px;
            color: #2c3e50;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .form-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .form-buttons button {
            flex: 1;
            padding: 10px;
        }
        
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .close:hover {
            color: #000;
        }
        
        .message {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            display: none;
        }
        
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }
        
        .action-buttons {
            display: flex;
            gap: 5px;
        }
        
        .action-buttons button {
            padding: 5px 10px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Library Book Records</h1>
            <p>Manage your library collection with ease</p>
        </div>
        
        <div class="button-group">
            <button class="btn-add" onclick="openAddModal()">➕ Add Book</button>
            <button class="btn-stats" onclick="toggleStats()">📊 Statistics</button>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search by title or author...">
            <button onclick="searchBooks()">🔍 Search</button>
            <button onclick="loadBooks()" style="background: #95a5a6;">Show All</button>
        </div>
        
        <div id="message" class="message"></div>
        
        <div id="statsContainer" style="display: none;">
            <div class="stats" id="statsContent"></div>
        </div>
        
        <div class="table-container">
            <table id="booksTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>ISBN</th>
                        <th>Year</th>
                        <th>Available</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div id="deleteModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeDeleteModal()">&times;</span>
            <h2>Delete Book</h2>
            <p>Are you sure you want to delete this book?</p>
            <p id="deleteBookName" style="font-weight: bold; color: #e74c3c;"></p>
            <div class="form-buttons">
                <button type="button" class="btn-delete" onclick="confirmDelete()">Yes, Delete</button>
                <button type="button" class="btn-add" onclick="closeDeleteModal()">Cancel</button>
            </div>
        </div>
    </div>
    
    <!-- Add Book Modal -->
    <div id="addModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeAddModal()">&times;</span>
            <h2>Add New Book</h2>
            <form onsubmit="addBook(event)">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="title" required>
                </div>
                <div class="form-group">
                    <label>Author(s)</label>
                    <input type="text" id="authors" required>
                </div>
                <div class="form-group">
                    <label>ISBN</label>
                    <input type="text" id="isbn" required>
                </div>
                <div class="form-group">
                    <label>Genres</label>
                    <input type="text" id="genres" placeholder="e.g., Fiction, Drama">
                </div>
                <div class="form-group">
                    <label>Publication Year</label>
                    <input type="number" id="year" value="2024">
                </div>
                <div class="form-group">
                    <label>Pages</label>
                    <input type="number" id="pages" value="0">
                </div>
                <div class="form-group">
                    <label>Publisher</label>
                    <input type="text" id="publisher">
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="description"></textarea>
                </div>
                <div class="form-group">
                    <label>Number of Copies</label>
                    <input type="number" id="copies" value="1" min="1">
                </div>
                <div class="form-buttons">
                    <button type="submit" class="btn-add">Add Book</button>
                    <button type="button" class="btn-delete" onclick="closeAddModal()">Cancel</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let allBooks = [];
        let bookToDelete = null;
        
        // Load books on page load
        window.onload = function() {
            loadBooks();
            // Add real-time search
            document.getElementById('searchInput').addEventListener('keyup', function() {
                if (this.value.length > 0) {
                    performSearch(this.value);
                } else {
                    displayBooks(allBooks);
                }
            });
        };
        
        function loadBooks() {
            fetch('/api/books')
                .then(response => response.json())
                .then(data => {
                    allBooks = data;
                    displayBooks(data);
                })
                .catch(error => showMessage('Error loading books', 'error'));
        }
        
        function performSearch(query) {
            if (!query) {
                displayBooks(allBooks);
                return;
            }
            
            // Local search for real-time filtering
            const filtered = allBooks.filter(book => {
                const title = (book[1] || '').toLowerCase();
                const author = (book[2] || '').toLowerCase();
                const isbn = (book[4] || '').toLowerCase();
                const searchTerm = query.toLowerCase();
                
                return title.includes(searchTerm) || 
                       author.includes(searchTerm) || 
                       isbn.includes(searchTerm);
            });
            
            displayBooks(filtered);
        }
        
        function displayBooks(books) {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            if (books.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px;">No books found</td></tr>';
                return;
            }
            
            books.forEach(book => {
                const row = document.createElement('tr');
                const bookId = book[0];
                const title = book[1];
                const author = book[2];
                const isbn = book[4];
                const year = book[5];
                const available = book[6];
                const total = book[7];
                
                row.innerHTML = `
                    <td>${bookId}</td>
                    <td><strong>${title}</strong></td>
                    <td>${author}</td>
                    <td>${isbn}</td>
                    <td>${year}</td>
                    <td>${available}/${total}</td>
                    <td>
                        <button class="btn-delete" onclick="openDeleteModal(${bookId}, '${title.replace(/'/g, "\\'")}')">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
        
        function searchBooks() {
            const query = document.getElementById('searchInput').value;
            performSearch(query);
        }
        
        function openAddModal() {
            document.getElementById('addModal').style.display = 'block';
        }
        
        function closeAddModal() {
            document.getElementById('addModal').style.display = 'none';
        }
        
        function openDeleteModal(bookId, title) {
            bookToDelete = bookId;
            document.getElementById('deleteBookName').textContent = `"${title}"`;
            document.getElementById('deleteModal').style.display = 'block';
        }
        
        function closeDeleteModal() {
            document.getElementById('deleteModal').style.display = 'none';
            bookToDelete = null;
        }
        
        function confirmDelete() {
            if (!bookToDelete) return;
            
            fetch(`/api/books/${bookToDelete}`, {method: 'DELETE'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showMessage('✓ Book deleted successfully!', 'success');
                        closeDeleteModal();
                        loadBooks();
                    } else {
                        showMessage('✗ Error: ' + data.error, 'error');
                    }
                })
                .catch(error => showMessage('Error deleting book', 'error'));
        }
        
        function addBook(event) {
            event.preventDefault();
            
            const bookData = {
                title: document.getElementById('title').value,
                authors: document.getElementById('authors').value,
                isbn: document.getElementById('isbn').value,
                genres: document.getElementById('genres').value,
                publication_year: parseInt(document.getElementById('year').value),
                pages: parseInt(document.getElementById('pages').value),
                publisher: document.getElementById('publisher').value,
                description: document.getElementById('description').value,
                total_copies: parseInt(document.getElementById('copies').value)
            };
            
            fetch('/api/books', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(bookData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('✓ Book added successfully!', 'success');
                    closeAddModal();
                    document.querySelector('form').reset();
                    loadBooks();
                } else {
                    showMessage('✗ Error: ' + data.error, 'error');
                }
            })
            .catch(error => showMessage('Error adding book', 'error'));
        }
        
        function toggleStats() {
            const container = document.getElementById('statsContainer');
            if (container.style.display === 'none') {
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        const html = `
                            <div class="stat-card">
                                <h3>📚 Total Books</h3>
                                <p>${data.total_books}</p>
                            </div>
                            <div class="stat-card">
                                <h3>📦 Total Copies</h3>
                                <p>${data.total_copies}</p>
                            </div>
                            <div class="stat-card">
                                <h3>✅ Available</h3>
                                <p>${data.available_copies}</p>
                            </div>
                            <div class="stat-card">
                                <h3>👥 Members</h3>
                                <p>${data.total_members}</p>
                            </div>
                            <div class="stat-card">
                                <h3>📋 Transactions</h3>
                                <p>${data.active_transactions}</p>
                            </div>
                        `;
                        document.getElementById('statsContent').innerHTML = html;
                        container.style.display = 'block';
                    });
            } else {
                container.style.display = 'none';
            }
        }
        
        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            setTimeout(() => msg.className = 'message', 4000);
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const addModal = document.getElementById('addModal');
            const deleteModal = document.getElementById('deleteModal');
            if (event.target == addModal) {
                addModal.style.display = 'none';
            }
            if (event.target == deleteModal) {
                deleteModal.style.display = 'none';
            }
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/books', methods=['GET'])
def get_books():
    db = get_db()
    books = db.get_all_books()
    books = convert_rows(books)
    db.disconnect()
    return jsonify(books)

@app.route('/api/search')
def search():
    db = get_db()
    query = request.args.get('q', '')
    results = db.search_books(query) if query else db.get_all_books()
    results = convert_rows(results)
    db.disconnect()
    return jsonify(results)

@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        db = get_db()
        data = request.json
        book_id = db.add_book(
            title=data.get('title'),
            authors=data.get('authors'),
            genres=data.get('genres'),
            isbn=data.get('isbn'),
            publication_year=data.get('publication_year', 2024),
            pages=data.get('pages', 0),
            description=data.get('description', ''),
            publisher=data.get('publisher', ''),
            total_copies=data.get('total_copies', 1)
        )
        db.disconnect()
        if book_id:
            return jsonify({'success': True, 'id': book_id})
        else:
            return jsonify({'success': False, 'error': 'Duplicate ISBN'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        db = get_db()
        query = "DELETE FROM books WHERE book_id = ?"
        db.execute_query(query, (book_id,))
        db.disconnect()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats')
def stats():
    db = get_db()
    result = db.get_database_stats()
    db.disconnect()
    return jsonify(result)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  LIBRARY MANAGEMENT SYSTEM - WEB VERSION")
    print("="*70)
    print("\n  🌐 Web interface running at: http://localhost:5000")
    print("\n  Features:")
    print("  ✅ View all books in a table")
    print("  ✅ Search books by title or author")
    print("  ✅ Add new books with full details")
    print("  ✅ Delete books")
    print("  ✅ View statistics")
    print("\n  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
