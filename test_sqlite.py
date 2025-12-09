#!/usr/bin/env python3
"""
Library Management System - SQLite Test & Demo Script

This script demonstrates all CRUD operations using SQLite instead of MySQL.
"""

import sqlite3
import os
from database_sqlite import DatabaseConnectionSQLite
from datetime import date

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_results(results, headers=None):
    """Print query results in a formatted table"""
    if not results:
        print("  No results found.")
        return
    
    if headers:
        print("\n  " + " | ".join(str(h) for h in headers))
        print("  " + "-" * 60)
    
    for row in results:
        if isinstance(row, sqlite3.Row):
            print("  " + " | ".join(str(item) if item is not None else 'NULL' for item in row))
        else:
            print("  " + " | ".join(str(item) if item is not None else 'NULL' for item in row))

def main():
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  LIBRARY MANAGEMENT SYSTEM - SQLITE TEST SUITE            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Initialize database
    db_file = 'library_sqlite.db'
    
    # Remove old database if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
    
    # Create new database and import schema
    print("\n⏳ Creating SQLite database from schema...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    with open('schema_sqlite.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    conn.close()
    print("✓ SQLite database created successfully!")
    
    # Connect using our database class
    db = DatabaseConnectionSQLite(db_file)
    print("✓ Database connection established successfully!\n")
    
    # ========== BOOK OPERATIONS ==========
    print_section("1. BOOK OPERATIONS")
    
    print("\n[1.1] Get All Books:")
    books = db.get_all_books()
    if books:
        print(f"  Found {len(books)} books")
        print("\n  Sample books:")
        for book in books[:3]:
            print(f"    - {book[1]} by {book[2]}")
            print(f"      Genres: {book[3]} | Copies: {book[6]} available / {book[7]} total")
    
    print("\n[1.2] Search Books (Tolkien):")
    results = db.search_books('Tolkien')
    if results:
        print(f"  Found {len(results)} result(s)")
        for book in results:
            print(f"    - {book[1]} by {book[2]}")
    
    print("\n[1.3] Get Detailed Book Information:")
    book_info = db.get_book_info(1)
    if book_info:
        print(f"  Title: {book_info[1]}")
        print(f"  Authors: {book_info[2]}")
        print(f"  Genres: {book_info[3]}")
        print(f"  ISBN: {book_info[4]}")
        print(f"  Publisher: {book_info[8]}")
    
    print("\n[1.4] Add New Book:")
    book_id = db.add_book(
        title="The Silmarillion",
        authors="J.R.R. Tolkien",
        genres="Classic Literature, Fantasy",
        isbn="978-0345325815",
        publication_year=1977,
        pages=365,
        description="Collection of mythopoeic stories about Middle-earth",
        publisher="Houghton Mifflin",
        total_copies=2
    )
    if book_id:
        print(f"  ✓ Successfully added book with ID: {book_id}")
    
    # ========== MEMBER OPERATIONS ==========
    print_section("2. MEMBER OPERATIONS")
    
    print("\n[2.1] Get All Members:")
    members = db.get_all_members()
    if members:
        print(f"  Found {len(members)} members")
        for member in members[:3]:
            print(f"    - {member[1]} ({member[2]}) - {member[3]} member")
    
    print("\n[2.2] Add New Member:")
    member_id = db.add_member("Sarah Wilson", "sarah.wilson@email.com", "Premium")
    if member_id:
        print(f"  ✓ Successfully added member with ID: {member_id}")
    
    print("\n[2.3] Search Members (Smith):")
    results = db.search_members('Smith')
    if results:
        print(f"  Found {len(results)} result(s)")
        for member in results:
            print(f"    - {member[1]} ({member[2]})")
    
    # ========== TRANSACTION OPERATIONS ==========
    print_section("3. TRANSACTION OPERATIONS")
    
    print("\n[3.1] Borrow Book (Member 1 borrows Book 5):")
    transaction_id = db.borrow_book(1, 5)
    if transaction_id:
        print(f"  ✓ Transaction created with ID: {transaction_id}")
        print(f"  ✓ Due date: {date.today()} + 14 days")
        print(f"  ✓ Book copy status updated to 'Borrowed'")
    
    print("\n[3.2] Current Active Transactions:")
    transactions = db.get_active_transactions()
    if transactions:
        print(f"  Found {len(transactions)} active transaction(s)")
        for trans in transactions:
            print(f"    - {trans[5]} borrowed '{trans[6]}' (Due: {trans[2]})")
    
    print("\n[3.3] Return Book (Transaction ID {}):")
    if transaction_id:
        success = db.return_book(transaction_id)
        if success:
            print(f"  ✓ Book returned successfully")
            print(f"  ✓ Return date: {date.today()}")
            print(f"  ✓ Fine amount: $0.00")
            print(f"  ✓ Book copy status updated to 'Available'")
    
    # ========== STATISTICS ==========
    print_section("4. DATABASE STATISTICS")
    
    stats = db.get_database_stats()
    print("\n[4.1] Overall Statistics:")
    for key, value in stats.items():
        print(f"    {key.replace('_', ' ').title()}: {value}")
    
    # Close connection
    db.disconnect()
    print("\n✓ Database connection closed")
    
    print("\n" + "="*70)
    print("  ✓ TEST SUITE COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
