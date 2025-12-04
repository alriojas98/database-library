# Library Management System

A comprehensive library management system demonstrating professional database design competencies (B.4 & C.6), featuring a fully normalized MySQL database, Python application server, and Tkinter GUI.

## 🎯 Project Competencies

This project demonstrates:

### **B.4: Relational Database Schema Design**
- Complete ER model with entities, relationships, and cardinalities
- Conceptual → Logical → Physical database design progression
- Comprehensive entity-relationship diagrams and documentation

### **C.6: Three-Stage Database Implementation**
1. **ER Design**: Conceptual model with 7 entities and multiple relationships
2. **Normalization**: Full 3NF normalization with justification and analysis
3. **Three-Tiered Architecture**:
   - **Tier 1**: MySQL Database Server (data storage and integrity)
   - **Tier 2**: Python Application Server (business logic - `database.py`)
   - **Tier 3**: Browser/Interface (Tkinter GUI - `library_app.py`)

## 📚 Features

### Core Functionality
- **Books**: Add, edit, delete, search with multi-author and multi-genre support
- **Members**: Manage library members with different membership types
- **Transactions**: Borrow and return books with automatic fine calculation
- **Relationships**: Many-to-many links between books-authors and books-genres
- **Advanced Search**: Search across titles, authors, genres, and ISBN
- **Availability Tracking**: Real-time tracking of book copies and their status

### Database Design Highlights
- **Normalized to 3NF**: Eliminates redundancy and ensures data integrity
- **8 Tables**: Publishers, Authors, Genres, Books, BookCopies, Members, Transactions, plus junction tables
- **2 Views**: Pre-built views for complex queries (`vw_books_complete`, `vw_active_transactions`)
- **Referential Integrity**: Foreign keys with CASCADE rules
- **Business Constraints**: Check constraints for date validation, status tracking
- **Optimized Indexes**: Strategic indexes on search fields and foreign keys

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Setup Instructions

### 1. Install Required Packages

```bash
pip install mysql-connector-python
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Database Setup

Make sure MySQL server is installed and running, then import the normalized schema:

```bash
# Connect to MySQL and create the database
mysql -u root -p < schema.sql
```

This will:
- Create the `librarydb` database
- Set up 8 normalized tables with proper relationships
- Create indexes and constraints
- Insert sample data (books, authors, members, transactions)
- Create views for simplified querying

### 3. Configuration

Edit `config.ini` to match your MySQL database settings:

```ini
[database]
host = localhost
user = your_mysql_username
password = your_mysql_password
database = librarydb
```

**Important**: Don't commit your actual password to version control!

## 🎮 Running the Application

### Option 1: Test Database Functionality (Recommended First)

Run the comprehensive test suite to verify the database setup:

```bash
python test_database.py
```

This will:
- Test all CRUD operations (Create, Read, Update, Delete)
- Demonstrate normalized relationships
- Test borrowing and returning books
- Calculate fines for overdue books
- Show database statistics and popular books
- Verify referential integrity

### Option 2: Launch GUI Application

Run the Tkinter interface for interactive use:

```bash
python library_app.py
```

or use the enhanced version with full CRUD features:

```bash
python library_app_new.py
```

The GUI provides:
- Browse and search all books
- Add, edit, and delete books
- View book availability and details
- Search by title, author, genre, or ISBN

### Option 3: Direct Database Interaction

For advanced users, interact directly with the database class:

```python
from database import DatabaseConnection

db = DatabaseConnection('config.ini')
db.connect()

# Search for books
books = db.search_books("Tolkien")

# Add a new member
member_id = db.add_member("John", "Doe", "john@email.com")

# Borrow a book
transaction_id = db.borrow_book(member_id=1, book_id=5, days=14)

# Return a book
return_info = db.return_book(transaction_id)
print(f"Fine: ${return_info['fine_amount']}")

db.disconnect()
```

## 📁 Project Structure

```
database-library/
├── DATABASE_DESIGN.md       # Complete design documentation (ER model, normalization)
├── README.md                 # This file
├── schema.sql                # Normalized database schema (3NF) with sample data
├── database.py               # Application server (Tier 2) - business logic
├── library_app.py            # Simple Tkinter GUI (Tier 3)
├── library_app_new.py        # Enhanced GUI with full CRUD operations
├── test_database.py          # Comprehensive test suite
├── config.ini                # Database configuration
├── requirements.txt          # Python dependencies
└── librarydb.mwb             # MySQL Workbench model file (optional)
```

## 📖 Documentation

### Complete Design Documentation

See **[DATABASE_DESIGN.md](DATABASE_DESIGN.md)** for:
- Complete ER diagram with all entities and relationships
- Normalization analysis (1NF → 2NF → 3NF)
- Entity-relationship details and cardinalities
- Three-tiered architecture explanation
- Design decisions and rationale

### Database Schema Overview

#### Core Entities
- **Books**: Title, ISBN, publication info, language, pages
- **Authors**: First/last name, bio, birth year
- **Publishers**: Name, country, website
- **Genres**: Name and description
- **BookCopies**: Physical copies with condition and location tracking
- **Members**: Library members with membership types
- **Transactions**: Borrowing history with dates and fines

#### Relationships
- **Book ↔ Author**: Many-to-Many (via `book_authors`)
- **Book ↔ Genre**: Many-to-Many (via `book_genres`)
- **Book → Publisher**: Many-to-One
- **Book → BookCopies**: One-to-Many
- **Member → Transactions**: One-to-Many
- **BookCopy → Transactions**: One-to-Many

## 🧪 Testing

Run the test suite to verify all functionality:

```bash
python test_database.py
```

**Test Coverage:**
1. ✓ Book Operations (search, add, update, delete)
2. ✓ Member Management (CRUD operations)
3. ✓ Transactions (borrow, return, fines)
4. ✓ Relationship Queries (many-to-many joins)
5. ✓ Advanced Features (statistics, popular books)

## 🎓 Educational Value

This project demonstrates professional competencies in:

1. **Database Design**: Complete ER modeling from problem statement
2. **Normalization**: Systematic elimination of redundancy (3NF)
3. **SQL**: DDL, DML, views, indexes, constraints
4. **Architecture**: Separation of concerns in 3-tier design
5. **Python**: OOP, database connectivity, error handling
6. **Software Engineering**: Modular design, documentation, testing

## 🔧 Troubleshooting

### Database Connection Errors
- Verify MySQL is running: `sudo service mysql status`
- Check credentials in `config.ini`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Schema Import Errors
- Make sure you're running the latest `schema.sql`
- Drop and recreate if needed: The schema file includes `DROP DATABASE IF EXISTS`

### Module Import Errors
- Install dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (requires 3.7+)

## 🚀 Future Enhancements

Potential additions to extend the project:
- [ ] Book reservations system
- [ ] User reviews and ratings
- [ ] Email notifications for due dates
- [ ] Web-based interface (Flask/Django)
- [ ] RESTful API for mobile apps
- [ ] Barcode scanning integration
- [ ] Late fee payment tracking
- [ ] Advanced analytics dashboard

## 📝 License

This project is created for educational purposes as part of database design coursework.

## 👥 Contributors

- Student Project - Database Design & Implementation (B.4 & C.6 Competencies)

---

**For complete design documentation, see [DATABASE_DESIGN.md](DATABASE_DESIGN.md)**

