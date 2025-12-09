import sqlite3
import os
from datetime import date, timedelta

class DatabaseConnectionSQLite:
    """
    SQLite version of the database connection handler for the library management system.
    
    This class provides the same functionality as the MySQL version but uses SQLite
    for easier setup and portability.
    """
    
    def __init__(self, db_file='library.db'):
        """
        Initialize the SQLite database connection
        
        Args:
            db_file (str): Path to the SQLite database file
        """
        self.db_file = db_file
        self.connection = None
        self.connect()
        
    def connect(self):
        """Establish a SQLite database connection"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"Error connecting to SQLite database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            
    def execute_query(self, query, params=None):
        """
        Execute a query with optional parameters
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
            
        Returns:
            list: Query results or None if error
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Check if query is a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
                
            cursor.close()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_all_books(self):
        """Get all books from the database"""
        query = "SELECT book_id, title, authors, genres, isbn, publication_year, available_copies, total_copies FROM books ORDER BY title"
        return self.execute_query(query) or []
    
    def search_books(self, search_term):
        """Search for books by title or author"""
        query = "SELECT book_id, title, authors, genres FROM books WHERE title LIKE ? OR authors LIKE ? ORDER BY title"
        params = (f"%{search_term}%", f"%{search_term}%")
        return self.execute_query(query, params) or []
    
    def get_book_info(self, book_id):
        """Get detailed information about a book"""
        query = "SELECT * FROM books WHERE book_id = ?"
        result = self.execute_query(query, (book_id,))
        return result[0] if result else None
    
    def add_book(self, title, authors, genres, isbn, publication_year, pages, description, publisher, total_copies):
        """Add a new book to the database"""
        query = """
        INSERT INTO books (title, authors, genres, isbn, publication_year, pages, description, publisher, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (title, authors, genres, isbn, publication_year, pages, description, publisher, total_copies, total_copies)
        return self.execute_query(query, params)
    
    def get_all_members(self):
        """Get all members from the database"""
        query = "SELECT member_id, name, email, member_type FROM members ORDER BY name"
        return self.execute_query(query) or []
    
    def search_members(self, search_term):
        """Search for members by name or email"""
        query = "SELECT member_id, name, email FROM members WHERE name LIKE ? OR email LIKE ? ORDER BY name"
        params = (f"%{search_term}%", f"%{search_term}%")
        return self.execute_query(query, params) or []
    
    def add_member(self, name, email, member_type="Standard"):
        """Add a new member to the database"""
        query = "INSERT INTO members (name, email, member_type) VALUES (?, ?, ?)"
        params = (name, email, member_type)
        return self.execute_query(query, params)
    
    def get_active_transactions(self):
        """Get all active transactions (borrowed books)"""
        query = """
        SELECT t.transaction_id, t.borrow_date, t.due_date, 
               CAST((julianday(t.due_date) - julianday('now')) AS INTEGER) as days_overdue,
               m.name, m.email, b.title, a.name as author, bc.copy_id, bc.status
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        JOIN book_copies bc ON t.copy_id = bc.copy_id
        JOIN books b ON bc.book_id = b.book_id
        LEFT JOIN authors a ON b.book_id = a.book_id
        WHERE t.return_date IS NULL
        ORDER BY t.due_date
        """
        return self.execute_query(query) or []
    
    def borrow_book(self, member_id, book_id, borrow_days=14):
        """Create a borrowing transaction"""
        try:
            # Get an available copy
            query = "SELECT copy_id FROM book_copies WHERE book_id = ? AND status = 'Available' LIMIT 1"
            result = self.execute_query(query, (book_id,))
            
            if not result:
                return None
            
            copy_id = result[0][0]
            today = date.today()
            due_date = today + timedelta(days=borrow_days)
            
            # Create transaction
            query = "INSERT INTO transactions (member_id, copy_id, borrow_date, due_date) VALUES (?, ?, ?, ?)"
            params = (member_id, copy_id, today, due_date)
            self.execute_query(query, params)
            
            # Update book copy status
            query = "UPDATE book_copies SET status = 'Borrowed' WHERE copy_id = ?"
            self.execute_query(query, (copy_id,))
            
            # Get the transaction ID
            query = "SELECT last_insert_rowid()"
            result = self.execute_query(query)
            return result[0][0] if result else None
            
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return None
    
    def return_book(self, transaction_id):
        """Return a borrowed book"""
        try:
            today = date.today()
            
            # Get transaction details
            query = "SELECT copy_id, due_date FROM transactions WHERE transaction_id = ?"
            result = self.execute_query(query, (transaction_id,))
            
            if not result:
                return False
            
            copy_id = result[0][0]
            due_date = result[0][1]
            
            # Calculate fine
            fine = 0.0
            if isinstance(due_date, str):
                due_date = date.fromisoformat(due_date)
            days_overdue = (today - due_date).days
            if days_overdue > 0:
                fine = days_overdue * 0.50  # $0.50 per day
            
            # Update transaction
            query = "UPDATE transactions SET return_date = ?, fine_amount = ? WHERE transaction_id = ?"
            self.execute_query(query, (today, fine, transaction_id))
            
            # Update book copy status
            query = "UPDATE book_copies SET status = 'Available' WHERE copy_id = ?"
            self.execute_query(query, (copy_id,))
            
            return True
            
        except Exception as e:
            print(f"Error returning book: {e}")
            return False
    
    def get_database_stats(self):
        """Get overall database statistics"""
        stats = {}
        
        # Total books
        query = "SELECT COUNT(*) as count FROM books"
        result = self.execute_query(query)
        stats['total_books'] = result[0][0] if result else 0
        
        # Total copies
        query = "SELECT COUNT(*) as count FROM book_copies"
        result = self.execute_query(query)
        stats['total_copies'] = result[0][0] if result else 0
        
        # Available copies
        query = "SELECT COUNT(*) as count FROM book_copies WHERE status = 'Available'"
        result = self.execute_query(query)
        stats['available_copies'] = result[0][0] if result else 0
        
        # Total members
        query = "SELECT COUNT(*) as count FROM members"
        result = self.execute_query(query)
        stats['total_members'] = result[0][0] if result else 0
        
        # Active transactions
        query = "SELECT COUNT(*) as count FROM transactions WHERE return_date IS NULL"
        result = self.execute_query(query)
        stats['active_transactions'] = result[0][0] if result else 0
        
        return stats
