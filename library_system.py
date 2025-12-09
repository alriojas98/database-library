#!/usr/bin/env python3
"""
Comprehensive Library Management System
Features:
- User authentication (admin, librarian, regular user)
- Book management (add, delete, update, search)
- Patron management
- Checkout/return system with fee calculations
- Admin dashboard
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class LibraryDatabase:
    """Handle library.db operations"""
    
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        if self.conn:
            self.conn.close()
            
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def fetch(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

class UserDatabase:
    """Handle usercred.db operations"""
    
    def __init__(self, db_name='usercred.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        if self.conn:
            self.conn.close()
            
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def fetch(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

class User(ABC):
    """Abstract base class for user roles"""
    
    def __init__(self, username, user_id, is_admin):
        self.username = username
        self.user_id = user_id
        self.is_admin = is_admin
        
    @abstractmethod
    def get_permissions(self):
        pass

class AdminUser(User):
    """Admin user with full permissions"""
    
    def get_permissions(self):
        return {
            'add_book': True,
            'delete_book': True,
            'update_book': True,
            'search_book': True,
            'manage_users': True,
            'view_reports': True,
            'checkout_book': True,
            'return_book': True,
            'manage_patrons': True
        }

class LibrarianUser(User):
    """Librarian user with book management permissions"""
    
    def get_permissions(self):
        return {
            'add_book': True,
            'delete_book': True,
            'update_book': True,
            'search_book': True,
            'manage_users': False,
            'view_reports': True,
            'checkout_book': True,
            'return_book': True,
            'manage_patrons': True
        }

class RegularUser(User):
    """Regular user with limited permissions"""
    
    def get_permissions(self):
        return {
            'add_book': False,
            'delete_book': False,
            'update_book': False,
            'search_book': True,
            'manage_users': False,
            'view_reports': False,
            'checkout_book': True,
            'return_book': True,
            'manage_patrons': False
        }

class AuthenticationManager:
    """Handle user authentication"""
    
    def __init__(self):
        self.user_db = UserDatabase()
        self.user_db.connect()
        self.current_user = None
        
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user and return User object"""
        result = self.user_db.fetch_one(
            'SELECT user_id, username, is_admin FROM Users WHERE username = ? AND password = ?',
            (username, self.hash_password(password))
        )
        
        if result:
            user_id, username, is_admin = result
            
            # Create appropriate user object based on admin status
            if is_admin:
                # Check if admin or librarian
                user = AdminUser(username, user_id, True)
            else:
                user = RegularUser(username, user_id, False)
            
            self.current_user = user
            
            # Update last login
            self.user_db.execute(
                'UPDATE Users SET last_login = ? WHERE user_id = ?',
                (datetime.now(), user_id)
            )
            
            return user
        
        return None
    
    def is_authenticated(self):
        return self.current_user is not None
    
    def logout(self):
        self.current_user = None

class LibraryManager:
    """Main library management system"""
    
    def __init__(self):
        self.lib_db = LibraryDatabase()
        self.lib_db.connect()
        self.auth = AuthenticationManager()
        
    def check_permission(self, permission):
        if not self.auth.is_authenticated():
            return False
        permissions = self.auth.current_user.get_permissions()
        return permissions.get(permission, False)
    
    # ========== BOOK OPERATIONS ==========
    
    def add_book(self, title, author, genre, isbn, publication_year, copies):
        if not self.check_permission('add_book'):
            return False, "Permission denied"
        
        try:
            self.lib_db.execute(
                '''INSERT INTO Books (title, author, genre, isbn, publication_year, copies_available)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (title, author, genre, isbn, publication_year, copies)
            )
            return True, "Book added successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_book(self, book_id):
        if not self.check_permission('delete_book'):
            return False, "Permission denied"
        
        try:
            self.lib_db.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))
            return True, "Book deleted successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def update_book(self, book_id, title=None, author=None, genre=None, copies=None):
        if not self.check_permission('update_book'):
            return False, "Permission denied"
        
        try:
            updates = []
            params = []
            
            if title:
                updates.append('title = ?')
                params.append(title)
            if author:
                updates.append('author = ?')
                params.append(author)
            if genre:
                updates.append('genre = ?')
                params.append(genre)
            if copies is not None:
                updates.append('copies_available = ?')
                params.append(copies)
            
            if not updates:
                return False, "No updates provided"
            
            params.append(book_id)
            query = f'UPDATE Books SET {", ".join(updates)} WHERE book_id = ?'
            self.lib_db.execute(query, params)
            return True, "Book updated successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def search_books(self, search_term):
        if not self.check_permission('search_book'):
            return None, "Permission denied"
        
        try:
            results = self.lib_db.fetch(
                '''SELECT book_id, title, author, genre, isbn, publication_year, copies_available
                   FROM Books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR isbn LIKE ?''',
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def get_all_books(self):
        try:
            results = self.lib_db.fetch(
                'SELECT book_id, title, author, genre, isbn, publication_year, copies_available FROM Books'
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    # ========== PATRON OPERATIONS ==========
    
    def add_patron(self, name, email, phone, address):
        try:
            self.lib_db.execute(
                '''INSERT INTO Patrons (name, email, phone, address)
                   VALUES (?, ?, ?, ?)''',
                (name, email, phone, address)
            )
            return True, "Patron added successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_all_patrons(self):
        try:
            results = self.lib_db.fetch(
                'SELECT patron_id, name, email, phone, address, membership_status FROM Patrons'
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def search_patrons(self, search_term):
        try:
            results = self.lib_db.fetch(
                '''SELECT patron_id, name, email, phone, address FROM Patrons
                   WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?''',
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    # ========== CHECKOUT/RETURN OPERATIONS ==========
    
    def checkout_book(self, patron_id, book_id, days=14):
        if not self.check_permission('checkout_book'):
            return False, "Permission denied"
        
        try:
            # Check book availability
            book = self.lib_db.fetch_one(
                'SELECT copies_available FROM Books WHERE book_id = ?',
                (book_id,)
            )
            
            if not book or book[0] <= 0:
                return False, "Book not available"
            
            checkout_date = datetime.now().date()
            due_date = checkout_date + timedelta(days=days)
            
            self.lib_db.execute(
                '''INSERT INTO Checkouts (patron_id, book_id, checkout_date, due_date, status)
                   VALUES (?, ?, ?, ?, ?)''',
                (patron_id, book_id, checkout_date, due_date, 'Active')
            )
            
            # Decrease available copies
            self.lib_db.execute(
                'UPDATE Books SET copies_available = copies_available - 1 WHERE book_id = ?',
                (book_id,)
            )
            
            return True, f"Book checked out. Due date: {due_date}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def return_book(self, checkout_id):
        if not self.check_permission('return_book'):
            return False, "Permission denied"
        
        try:
            # Get checkout info
            checkout = self.lib_db.fetch_one(
                'SELECT book_id, due_date FROM Checkouts WHERE checkout_id = ? AND status = ?',
                (checkout_id, 'Active')
            )
            
            if not checkout:
                return False, "Checkout not found or already returned"
            
            book_id, due_date = checkout
            return_date = datetime.now().date()
            fee = 0.0
            
            # Calculate late fees ($0.50 per day)
            if return_date > due_date:
                days_late = (return_date - due_date).days
                fee = days_late * 0.50
            
            # Update checkout
            self.lib_db.execute(
                'UPDATE Checkouts SET return_date = ?, fee = ?, status = ? WHERE checkout_id = ?',
                (return_date, fee, 'Returned', checkout_id)
            )
            
            # Increase available copies
            self.lib_db.execute(
                'UPDATE Books SET copies_available = copies_available + 1 WHERE book_id = ?',
                (book_id,)
            )
            
            fee_msg = f" (Late fee: ${fee:.2f})" if fee > 0 else ""
            return True, f"Book returned successfully{fee_msg}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_active_checkouts(self):
        try:
            results = self.lib_db.fetch(
                '''SELECT c.checkout_id, p.name, b.title, c.checkout_date, c.due_date, c.status
                   FROM Checkouts c
                   JOIN Patrons p ON c.patron_id = p.patron_id
                   JOIN Books b ON c.book_id = b.book_id
                   WHERE c.status = 'Active'
                   ORDER BY c.due_date'''
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def get_overdue_books(self):
        try:
            today = datetime.now().date()
            results = self.lib_db.fetch(
                '''SELECT c.checkout_id, p.name, b.title, c.due_date, 
                          CAST((julianday(?) - julianday(c.due_date)) AS INTEGER) as days_late
                   FROM Checkouts c
                   JOIN Patrons p ON c.patron_id = p.patron_id
                   JOIN Books b ON c.book_id = b.book_id
                   WHERE c.status = 'Active' AND c.due_date < ?
                   ORDER BY c.due_date''',
                (today, today)
            )
            return results, None
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def disconnect(self):
        self.lib_db.disconnect()
        self.auth.user_db.disconnect()

def display_menu(user):
    """Display menu based on user role"""
    print("\n" + "="*70)
    print(f"  LIBRARY MANAGEMENT SYSTEM - {user.username.upper()}")
    print("="*70)
    
    perms = user.get_permissions()
    
    print("\n📚 LIBRARY OPERATIONS:")
    if perms['search_book']:
        print("  1. Search Books")
    if perms['add_book']:
        print("  2. Add Book")
    if perms['update_book']:
        print("  3. Update Book")
    if perms['delete_book']:
        print("  4. Delete Book")
    if perms['checkout_book']:
        print("  5. Checkout Book")
    if perms['return_book']:
        print("  6. Return Book")
    
    print("\n👥 PATRON OPERATIONS:")
    if perms['manage_patrons']:
        print("  7. Add Patron")
        print("  8. View Patrons")
        print("  9. Search Patrons")
    
    print("\n📊 REPORTS:")
    if perms['checkout_book']:
        print("  10. View Active Checkouts")
    if perms['view_reports']:
        print("  11. View Overdue Books")
        print("  12. View All Books")
    
    print("\n" + "-"*70)
    print("  0. Logout")
    print("="*70)

def main():
    """Main application loop"""
    manager = LibraryManager()
    
    print("\n" + "="*70)
    print("  LIBRARY MANAGEMENT SYSTEM")
    print("="*70)
    
    while True:
        if not manager.auth.is_authenticated():
            print("\n🔐 LOGIN")
            print("-"*70)
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            user = manager.auth.authenticate(username, password)
            if user:
                print(f"\n✓ Welcome, {user.username}!")
            else:
                print("\n✗ Invalid credentials")
                continue
        
        user = manager.auth.current_user
        display_menu(user)
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '0':
            print("\n✓ Logged out")
            manager.auth.logout()
        
        elif choice == '1':
            search_term = input("\nSearch term: ").strip()
            books, error = manager.search_books(search_term)
            if error:
                print(f"\n✗ {error}")
            else:
                print(f"\n📚 Found {len(books)} book(s):")
                for book in books:
                    print(f"  ID: {book[0]:2d} | {book[1]:<30s} | {book[2]:<20s} | Available: {book[6]}")
        
        elif choice == '2':
            if not user.get_permissions()['add_book']:
                print("\n✗ Permission denied")
            else:
                print("\n📖 ADD BOOK")
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                genre = input("Genre: ").strip()
                isbn = input("ISBN: ").strip()
                year = int(input("Publication Year: ").strip())
                copies = int(input("Number of Copies: ").strip())
                
                success, msg = manager.add_book(title, author, genre, isbn, year, copies)
                print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '3':
            if not user.get_permissions()['update_book']:
                print("\n✗ Permission denied")
            else:
                book_id = int(input("\nBook ID to update: ").strip())
                print("(Leave blank to skip a field)")
                title = input("New Title: ").strip() or None
                author = input("New Author: ").strip() or None
                genre = input("New Genre: ").strip() or None
                
                success, msg = manager.update_book(book_id, title, author, genre)
                print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '4':
            if not user.get_permissions()['delete_book']:
                print("\n✗ Permission denied")
            else:
                book_id = int(input("\nBook ID to delete: ").strip())
                success, msg = manager.delete_book(book_id)
                print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '5':
            patron_id = int(input("\nPatron ID: ").strip())
            book_id = int(input("Book ID: ").strip())
            success, msg = manager.checkout_book(patron_id, book_id)
            print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '6':
            checkout_id = int(input("\nCheckout ID: ").strip())
            success, msg = manager.return_book(checkout_id)
            print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '7':
            if not user.get_permissions()['manage_patrons']:
                print("\n✗ Permission denied")
            else:
                print("\n👤 ADD PATRON")
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                address = input("Address: ").strip()
                
                success, msg = manager.add_patron(name, email, phone, address)
                print(f"\n{'✓' if success else '✗'} {msg}")
        
        elif choice == '8':
            if not user.get_permissions()['manage_patrons']:
                print("\n✗ Permission denied")
            else:
                patrons, error = manager.get_all_patrons()
                if error:
                    print(f"\n✗ {error}")
                else:
                    print(f"\n👥 Patrons ({len(patrons)}):")
                    for patron in patrons:
                        print(f"  ID: {patron[0]:2d} | {patron[1]:<20s} | {patron[2]:<25s} | {patron[5]}")
        
        elif choice == '9':
            if not user.get_permissions()['manage_patrons']:
                print("\n✗ Permission denied")
            else:
                search_term = input("\nSearch term: ").strip()
                patrons, error = manager.search_patrons(search_term)
                if error:
                    print(f"\n✗ {error}")
                else:
                    print(f"\n👥 Found {len(patrons)} patron(s):")
                    for patron in patrons:
                        print(f"  ID: {patron[0]:2d} | {patron[1]:<20s} | {patron[2]}")
        
        elif choice == '10':
            checkouts, error = manager.get_active_checkouts()
            if error:
                print(f"\n✗ {error}")
            else:
                print(f"\n📋 Active Checkouts ({len(checkouts)}):")
                for checkout in checkouts:
                    print(f"  ID: {checkout[0]:3d} | {checkout[1]:<15s} | {checkout[2]:<30s} | Due: {checkout[4]}")
        
        elif choice == '11':
            if not user.get_permissions()['view_reports']:
                print("\n✗ Permission denied")
            else:
                overdue, error = manager.get_overdue_books()
                if error:
                    print(f"\n✗ {error}")
                else:
                    if not overdue:
                        print("\n✓ No overdue books")
                    else:
                        print(f"\n⚠️  Overdue Books ({len(overdue)}):")
                        for book in overdue:
                            print(f"  ID: {book[0]:3d} | {book[1]:<15s} | {book[2]:<30s} | {book[4]} days late")
        
        elif choice == '12':
            if not user.get_permissions()['view_reports']:
                print("\n✗ Permission denied")
            else:
                books, error = manager.get_all_books()
                if error:
                    print(f"\n✗ {error}")
                else:
                    print(f"\n📚 All Books ({len(books)}):")
                    for book in books:
                        print(f"  ID: {book[0]:2d} | {book[1]:<30s} | {book[2]:<20s} | Available: {book[6]}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Application closed")
    except Exception as e:
        print(f"\n✗ Error: {e}")
