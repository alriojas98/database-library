import mysql.connector
from mysql.connector import Error
import configparser
import os
from datetime import date, timedelta

class DatabaseConnection:
    """
    A comprehensive database connection and operations handler for the library management system.
    
    This class implements the application server layer (Tier 2) of the three-tiered architecture,
    providing business logic and data access methods for the normalized database schema.
    
    Features:
    - Connection management with configuration file support
    - CRUD operations for all entities (books, authors, members, transactions, etc.)
    - Advanced search and filtering capabilities
    - Transaction management for borrowing and returning books
    - Fine calculations for overdue books
    - Comprehensive error handling
    """
    
    def __init__(self, config_file='config.ini'):
        """
        Initialize the database connection using the config file
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.connection = None
        self.config_file = config_file
        self.db_config = self._read_config()
        
    def _read_config(self):
        """Read database configuration from config file"""
        config = configparser.ConfigParser()
        
        # Check if config file exists
        if not os.path.exists(self.config_file):
            # Use default configuration
            return {
                'host': 'localhost',
                'user': 'root',
                'password': 'password',
                'database': 'librarydb'
            }
        
        # Read configuration file
        config.read(self.config_file)
        return {
            'host': config['database']['host'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'database': config['database']['database']
        }
        
    def connect(self):
        """Establish a database connection"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
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
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
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
            
        except Error as e:
            print(f"Error executing query: {e}")
            return None
            
    # ========================================================================
    # BOOK OPERATIONS (utilizing normalized schema with views)
    # ========================================================================
    
    def get_all_books(self):
        """
        Get all books from the database using the complete view
        
        Returns:
            list: List of tuples containing book information
        """
        query = """
            SELECT book_id, title, authors, genres, publication_year, 
                   publisher, total_copies, available_copies
            FROM vw_books_complete
            ORDER BY title
        """
        return self.execute_query(query)
    
    def get_book_details(self, book_id):
        """
        Get detailed information for a specific book
        
        Args:
            book_id (int): ID of the book
            
        Returns:
            dict: Book details or None if not found
        """
        query = """
            SELECT book_id, title, authors, genres, isbn, publication_year,
                   language, pages, description, publisher, 
                   total_copies, available_copies
            FROM vw_books_complete
            WHERE book_id = %s
        """
        result = self.execute_query(query, (book_id,))
        if result and len(result) > 0:
            return {
                'book_id': result[0][0],
                'title': result[0][1],
                'authors': result[0][2],
                'genres': result[0][3],
                'isbn': result[0][4],
                'publication_year': result[0][5],
                'language': result[0][6],
                'pages': result[0][7],
                'description': result[0][8],
                'publisher': result[0][9],
                'total_copies': result[0][10],
                'available_copies': result[0][11]
            }
        return None
        
    def search_books(self, search_term):
        """
        Search for books by title, author, genre, or ISBN
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: Matching books
        """
        query = """
            SELECT book_id, title, authors, genres, publication_year,
                   publisher, total_copies, available_copies
            FROM vw_books_complete
            WHERE title LIKE %s 
               OR authors LIKE %s 
               OR genres LIKE %s
               OR isbn LIKE %s
            ORDER BY title
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern, 
                                         search_pattern, search_pattern))
    
    def add_book(self, title, isbn, publication_year, publisher_name, 
                 language='English', pages=None, description=None,
                 author_names=None, genre_names=None, num_copies=1):
        """
        Add a new book to the database with authors, genres, and copies
        
        Args:
            title (str): Book title
            isbn (str): ISBN number
            publication_year (int): Year of publication
            publisher_name (str): Publisher name
            language (str): Book language
            pages (int): Number of pages
            description (str): Book description
            author_names (list): List of author names as tuples [(first, last), ...]
            genre_names (list): List of genre names
            num_copies (int): Number of physical copies to add
            
        Returns:
            int: ID of the new book or None if error
        """
        try:
            # Get or create publisher
            publisher_id = self._get_or_create_publisher(publisher_name)
            
            # Insert book
            query = """
                INSERT INTO books (title, isbn, publication_year, publisher_id, 
                                 language, pages, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (title, isbn, publication_year, publisher_id, 
                     language, pages, description)
            
            if self.execute_query(query, params) is None:
                return None
                
            book_id = self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
            
            # Link authors
            if author_names:
                for order, (first_name, last_name) in enumerate(author_names, 1):
                    author_id = self._get_or_create_author(first_name, last_name)
                    self.execute_query(
                        "INSERT INTO book_authors (book_id, author_id, author_order) VALUES (%s, %s, %s)",
                        (book_id, author_id, order)
                    )
            
            # Link genres
            if genre_names:
                for genre_name in genre_names:
                    genre_id = self._get_or_create_genre(genre_name)
                    self.execute_query(
                        "INSERT INTO book_genres (book_id, genre_id) VALUES (%s, %s)",
                        (book_id, genre_id)
                    )
            
            # Add book copies
            for _ in range(num_copies):
                self.execute_query(
                    "INSERT INTO book_copies (book_id, status) VALUES (%s, 'Available')",
                    (book_id,)
                )
            
            return book_id
            
        except Error as e:
            print(f"Error adding book: {e}")
            return None
    
    def update_book(self, book_id, title, isbn, publication_year, publisher_name,
                   language='English', pages=None, description=None):
        """
        Update an existing book's basic information
        
        Args:
            book_id (int): ID of the book to update
            title (str): Book title
            isbn (str): ISBN number
            publication_year (int): Year of publication
            publisher_name (str): Publisher name
            language (str): Book language
            pages (int): Number of pages
            description (str): Book description
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            publisher_id = self._get_or_create_publisher(publisher_name)
            
            query = """
                UPDATE books
                SET title = %s, isbn = %s, publication_year = %s, 
                    publisher_id = %s, language = %s, pages = %s, description = %s
                WHERE book_id = %s
            """
            params = (title, isbn, publication_year, publisher_id, 
                     language, pages, description, book_id)
            
            return self.execute_query(query, params) is not None
            
        except Error as e:
            print(f"Error updating book: {e}")
            return False
        
    def delete_book(self, book_id):
        """
        Delete a book and all associated records (cascades to copies, authors, genres)
        
        Args:
            book_id (int): ID of the book to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "DELETE FROM books WHERE book_id = %s"
        return self.execute_query(query, (book_id,)) is not None
    
    # ========================================================================
    # MEMBER OPERATIONS
    # ========================================================================
    
    def get_all_members(self):
        """Get all library members"""
        query = """
            SELECT member_id, first_name, last_name, email, phone, 
                   membership_type, status
            FROM members
            ORDER BY last_name, first_name
        """
        return self.execute_query(query)
    
    def add_member(self, first_name, last_name, email, phone=None, 
                  address=None, membership_type='Standard'):
        """
        Add a new library member
        
        Args:
            first_name (str): Member's first name
            last_name (str): Member's last name
            email (str): Member's email
            phone (str): Member's phone number
            address (str): Member's address
            membership_type (str): Type of membership
            
        Returns:
            int: ID of the new member or None if error
        """
        query = """
            INSERT INTO members (first_name, last_name, email, phone, 
                               address, membership_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, phone, address, membership_type)
        
        if self.execute_query(query, params) is not None:
            return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
        return None
    
    def search_members(self, search_term):
        """Search members by name or email"""
        query = """
            SELECT member_id, first_name, last_name, email, phone,
                   membership_type, status
            FROM members
            WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
            ORDER BY last_name, first_name
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))
    
    # ========================================================================
    # TRANSACTION OPERATIONS (Borrowing & Returning)
    # ========================================================================
    
    def borrow_book(self, member_id, book_id, days=14):
        """
        Create a borrowing transaction for a member
        
        Args:
            member_id (int): ID of the member
            book_id (int): ID of the book
            days (int): Number of days for the loan period
            
        Returns:
            int: Transaction ID or None if no available copies
        """
        try:
            # Find an available copy
            query = """
                SELECT copy_id FROM book_copies
                WHERE book_id = %s AND status = 'Available'
                LIMIT 1
            """
            result = self.execute_query(query, (book_id,))
            
            if not result or len(result) == 0:
                return None  # No available copies
            
            copy_id = result[0][0]
            
            # Create transaction
            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=days)
            
            query = """
                INSERT INTO transactions (member_id, copy_id, borrow_date, due_date, status)
                VALUES (%s, %s, %s, %s, 'Active')
            """
            if self.execute_query(query, (member_id, copy_id, borrow_date, due_date)) is None:
                return None
            
            # Update copy status
            self.execute_query(
                "UPDATE book_copies SET status = 'Borrowed' WHERE copy_id = %s",
                (copy_id,)
            )
            
            return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
            
        except Error as e:
            print(f"Error borrowing book: {e}")
            return None
    
    def return_book(self, transaction_id):
        """
        Process the return of a borrowed book
        
        Args:
            transaction_id (int): ID of the transaction
            
        Returns:
            dict: Return info with fine amount, or None if error
        """
        try:
            # Get transaction details
            query = """
                SELECT copy_id, due_date, status
                FROM transactions
                WHERE transaction_id = %s
            """
            result = self.execute_query(query, (transaction_id,))
            
            if not result or len(result) == 0:
                return None
            
            copy_id, due_date, status = result[0]
            
            if status != 'Active':
                return None  # Already returned
            
            # Calculate fine if overdue
            return_date = date.today()
            fine_amount = 0.0
            
            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine_amount = days_overdue * 0.50  # $0.50 per day
            
            # Update transaction
            query = """
                UPDATE transactions
                SET return_date = %s, fine_amount = %s, status = 'Returned'
                WHERE transaction_id = %s
            """
            self.execute_query(query, (return_date, fine_amount, transaction_id))
            
            # Update copy status
            self.execute_query(
                "UPDATE book_copies SET status = 'Available' WHERE copy_id = %s",
                (copy_id,)
            )
            
            return {
                'transaction_id': transaction_id,
                'return_date': return_date,
                'fine_amount': fine_amount
            }
            
        except Error as e:
            print(f"Error returning book: {e}")
            return None
    
    def get_active_transactions(self):
        """Get all active borrowing transactions"""
        query = "SELECT * FROM vw_active_transactions ORDER BY due_date"
        return self.execute_query(query)
    
    def get_member_transactions(self, member_id):
        """Get borrowing history for a specific member"""
        query = """
            SELECT t.transaction_id, b.title, t.borrow_date, t.due_date,
                   t.return_date, t.fine_amount, t.status
            FROM transactions t
            JOIN book_copies bc ON t.copy_id = bc.copy_id
            JOIN books b ON bc.book_id = b.book_id
            WHERE t.member_id = %s
            ORDER BY t.borrow_date DESC
        """
        return self.execute_query(query, (member_id,))
    
    # ========================================================================
    # UTILITY / HELPER METHODS
    # ========================================================================
    
    def _get_or_create_publisher(self, name):
        """Get publisher ID or create new publisher"""
        query = "SELECT publisher_id FROM publishers WHERE name = %s"
        result = self.execute_query(query, (name,))
        
        if result and len(result) > 0:
            return result[0][0]
        
        # Create new publisher
        self.execute_query("INSERT INTO publishers (name) VALUES (%s)", (name,))
        return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
    
    def _get_or_create_author(self, first_name, last_name):
        """Get author ID or create new author"""
        query = """
            SELECT author_id FROM authors 
            WHERE first_name = %s AND last_name = %s
        """
        result = self.execute_query(query, (first_name, last_name))
        
        if result and len(result) > 0:
            return result[0][0]
        
        # Create new author
        self.execute_query(
            "INSERT INTO authors (first_name, last_name) VALUES (%s, %s)",
            (first_name, last_name)
        )
        return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
    
    def _get_or_create_genre(self, name):
        """Get genre ID or create new genre"""
        query = "SELECT genre_id FROM genres WHERE name = %s"
        result = self.execute_query(query, (name,))
        
        if result and len(result) > 0:
            return result[0][0]
        
        # Create new genre
        self.execute_query("INSERT INTO genres (name) VALUES (%s)", (name,))
        return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
    
    def get_all_authors(self):
        """Get all authors"""
        query = "SELECT author_id, first_name, last_name FROM authors ORDER BY last_name"
        return self.execute_query(query)
    
    def get_all_genres(self):
        """Get all genres"""
        query = "SELECT genre_id, name FROM genres ORDER BY name"
        return self.execute_query(query)
    
    def get_all_publishers(self):
        """Get all publishers"""
        query = "SELECT publisher_id, name FROM publishers ORDER BY name"
        return self.execute_query(query)