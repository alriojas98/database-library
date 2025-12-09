#!/usr/bin/env python3
"""
Interactive Library Management System
Allows users to manage books, members, and transactions interactively
"""

from database_sqlite import DatabaseConnectionSQLite
from datetime import date, timedelta

class LibraryInteractive:
    def __init__(self):
        self.db = DatabaseConnectionSQLite('library_sqlite.db')
        self.running = True
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("  LIBRARY MANAGEMENT SYSTEM - INTERACTIVE MODE")
        print("="*70)
        print("\n  📚 MAIN MENU:")
        print("  1. View All Books")
        print("  2. Search Books")
        print("  3. Add New Book")
        print("  4. Delete Book")
        print("  5. View All Members")
        print("  6. Add New Member")
        print("  7. Borrow Book")
        print("  8. Return Book")
        print("  9. View Active Transactions")
        print("  10. Database Statistics")
        print("  0. Exit")
        print("="*70)
    
    def view_all_books(self):
        """Display all books in the library"""
        print("\n📚 ALL BOOKS IN LIBRARY:")
        print("-" * 70)
        books = self.db.get_all_books()
        if not books:
            print("  No books found!")
            return
        
        for book in books:
            book_id, title, authors, genres, isbn, pub_year, avail, total = book
            print(f"  ID: {book_id} | {title}")
            print(f"     By: {authors} | Year: {pub_year}")
            print(f"     ISBN: {isbn}")
            print(f"     Available: {avail}/{total} copies")
            print()
    
    def search_books(self):
        """Search for books"""
        print("\n🔍 SEARCH BOOKS:")
        print("-" * 70)
        query = input("  Enter search term (title or author): ").strip()
        
        if not query:
            print("  Search cancelled.")
            return
        
        results = self.db.search_books(query)
        if not results:
            print(f"  No books found matching '{query}'")
            return
        
        print(f"\n  Found {len(results)} book(s):")
        for book in results:
            book_id, title, authors, genres = book
            print(f"  ID: {book_id} | {title} by {authors}")
    
    def add_book(self):
        """Add a new book to the library"""
        print("\n➕ ADD NEW BOOK:")
        print("-" * 70)
        
        try:
            title = input("  Enter book title: ").strip()
            if not title:
                print("  ✗ Title cannot be empty!")
                return
            
            authors = input("  Enter author(s): ").strip()
            if not authors:
                authors = "Unknown"
            
            isbn = input("  Enter ISBN: ").strip()
            if not isbn:
                isbn = f"AUTO-{date.today()}"
            
            genres = input("  Enter genres (comma-separated): ").strip()
            if not genres:
                genres = "General"
            
            pub_year_str = input("  Enter publication year (or press Enter for current year): ").strip()
            pub_year = int(pub_year_str) if pub_year_str else date.today().year
            
            pages_str = input("  Enter number of pages (or press Enter for 0): ").strip()
            pages = int(pages_str) if pages_str else 0
            
            description = input("  Enter book description: ").strip()
            if not description:
                description = "No description available"
            
            publisher = input("  Enter publisher: ").strip()
            if not publisher:
                publisher = "Unknown"
            
            copies_str = input("  Enter number of copies to add (default 1): ").strip()
            copies = int(copies_str) if copies_str else 1
            
            # Add book to database
            book_id = self.db.add_book(
                title=title,
                authors=authors,
                genres=genres,
                isbn=isbn,
                publication_year=pub_year,
                pages=pages,
                description=description,
                publisher=publisher,
                total_copies=copies
            )
            
            if book_id:
                print(f"\n  ✓ Book added successfully!")
                print(f"  ✓ Book ID: {book_id}")
                print(f"  ✓ Title: {title}")
                print(f"  ✓ Copies added: {copies}")
            else:
                print(f"  ✗ Failed to add book (duplicate ISBN?)")
        
        except ValueError:
            print("  ✗ Invalid input! Please check your entries.")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def delete_book(self):
        """Delete a book from the library"""
        print("\n❌ DELETE BOOK:")
        print("-" * 70)
        
        try:
            # First show all books
            books = self.db.get_all_books()
            if not books:
                print("  No books to delete!")
                return
            
            print("\n  Available books:")
            for book in books[:10]:
                print(f"  ID: {book[0]:2d} | {book[1]} ({book[2]})")
            if len(books) > 10:
                print(f"  ... and {len(books)-10} more")
            
            book_id_str = input("\n  Enter book ID to delete: ").strip()
            book_id = int(book_id_str)
            
            # Check if book exists
            book_info = self.db.get_book_info(book_id)
            if not book_info:
                print(f"  ✗ Book ID {book_id} not found!")
                return
            
            # Confirm deletion
            print(f"\n  Book to delete: {book_info[1]}")
            confirm = input("  Are you sure? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                # Delete from database
                query = "DELETE FROM books WHERE book_id = ?"
                self.db.execute_query(query, (book_id,))
                print(f"  ✓ Book deleted successfully!")
            else:
                print("  Deletion cancelled.")
        
        except ValueError:
            print("  ✗ Invalid book ID!")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def view_all_members(self):
        """Display all members"""
        print("\n👥 ALL MEMBERS:")
        print("-" * 70)
        members = self.db.get_all_members()
        if not members:
            print("  No members found!")
            return
        
        for member in members:
            member_id, name, email, member_type = member
            print(f"  ID: {member_id} | {name} ({member_type})")
            print(f"     Email: {email}\n")
    
    def add_member(self):
        """Add a new member"""
        print("\n➕ ADD NEW MEMBER:")
        print("-" * 70)
        
        try:
            name = input("  Enter member name: ").strip()
            if not name:
                print("  ✗ Name cannot be empty!")
                return
            
            email = input("  Enter email: ").strip()
            if not email:
                print("  ✗ Email cannot be empty!")
                return
            
            print("\n  Member types: Standard, Premium, Student")
            member_type = input("  Enter member type (default: Standard): ").strip()
            if not member_type:
                member_type = "Standard"
            
            member_id = self.db.add_member(name, email, member_type)
            if member_id:
                print(f"\n  ✓ Member added successfully!")
                print(f"  ✓ Member ID: {member_id}")
                print(f"  ✓ Name: {name}")
                print(f"  ✓ Type: {member_type}")
            else:
                print("  ✗ Failed to add member (duplicate email?)")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def borrow_book(self):
        """Borrow a book"""
        print("\n📖 BORROW BOOK:")
        print("-" * 70)
        
        try:
            # Show members
            members = self.db.get_all_members()
            print("\n  Available members:")
            for member in members[:5]:
                print(f"  ID: {member[0]} | {member[1]}")
            if len(members) > 5:
                print(f"  ... and {len(members)-5} more")
            
            member_id_str = input("\n  Enter member ID: ").strip()
            member_id = int(member_id_str)
            
            # Show books
            books = self.db.get_all_books()
            print("\n  Available books:")
            for book in books[:5]:
                if book[6] > 0:  # Only show if copies available
                    print(f"  ID: {book[0]:2d} | {book[1]} ({book[6]} available)")
            if len(books) > 5:
                print(f"  ... and more")
            
            book_id_str = input("\n  Enter book ID: ").strip()
            book_id = int(book_id_str)
            
            transaction_id = self.db.borrow_book(member_id, book_id)
            if transaction_id:
                due_date = date.today() + timedelta(days=14)
                print(f"\n  ✓ Book borrowed successfully!")
                print(f"  ✓ Transaction ID: {transaction_id}")
                print(f"  ✓ Due date: {due_date}")
            else:
                print("  ✗ Failed to borrow book (no copies available?)")
        
        except ValueError:
            print("  ✗ Invalid ID!")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def return_book(self):
        """Return a borrowed book"""
        print("\n📚 RETURN BOOK:")
        print("-" * 70)
        
        try:
            # Show active transactions
            trans = self.db.get_active_transactions()
            if not trans:
                print("  No active transactions!")
                return
            
            print("\n  Active borrowings:")
            shown = 0
            for t in trans:
                print(f"  ID: {t[0]} | {t[5]} - '{t[6]}'")
                shown += 1
                if shown >= 5:
                    break
            
            if len(trans) > 5:
                print(f"  ... and {len(trans)-5} more")
            
            trans_id_str = input("\n  Enter transaction ID to return: ").strip()
            trans_id = int(trans_id_str)
            
            success = self.db.return_book(trans_id)
            if success:
                print(f"\n  ✓ Book returned successfully!")
                print(f"  ✓ Return date: {date.today()}")
                print(f"  ✓ Book available for checkout")
            else:
                print("  ✗ Failed to return book")
        
        except ValueError:
            print("  ✗ Invalid transaction ID!")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def view_transactions(self):
        """View active transactions"""
        print("\n📋 ACTIVE TRANSACTIONS:")
        print("-" * 70)
        trans = self.db.get_active_transactions()
        if not trans:
            print("  No active transactions!")
            return
        
        print(f"\n  Found {len(trans)} active transaction(s):\n")
        for t in trans:
            print(f"  Transaction ID: {t[0]}")
            print(f"  Member: {t[5]} ({t[4]})")
            print(f"  Book: {t[6]} by {t[7]}")
            print(f"  Borrow Date: {t[1]}")
            print(f"  Due Date: {t[2]} ({t[3]} days)")
            print()
    
    def view_statistics(self):
        """View database statistics"""
        print("\n📊 LIBRARY STATISTICS:")
        print("-" * 70)
        stats = self.db.get_database_stats()
        
        print(f"\n  Total Books: {stats['total_books']}")
        print(f"  Total Book Copies: {stats['total_copies']}")
        print(f"  Available Copies: {stats['available_copies']}")
        print(f"  Total Members: {stats['total_members']}")
        print(f"  Active Transactions: {stats['active_transactions']}")
    
    def run(self):
        """Main program loop"""
        while self.running:
            self.display_menu()
            choice = input("\n  Enter choice (0-10): ").strip()
            
            if choice == '0':
                print("\n  Goodbye! 👋\n")
                self.running = False
            elif choice == '1':
                self.view_all_books()
            elif choice == '2':
                self.search_books()
            elif choice == '3':
                self.add_book()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                self.view_all_members()
            elif choice == '6':
                self.add_member()
            elif choice == '7':
                self.borrow_book()
            elif choice == '8':
                self.return_book()
            elif choice == '9':
                self.view_transactions()
            elif choice == '10':
                self.view_statistics()
            else:
                print("\n  ✗ Invalid choice! Please try again.")
        
        self.db.disconnect()

if __name__ == "__main__":
    app = LibraryInteractive()
    app.run()
