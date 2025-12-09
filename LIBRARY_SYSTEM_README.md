# Library Management System - Complete Guide

## Overview
A comprehensive, role-based library management system with two SQLite databases:
- **library.db**: Books, Patrons, and Checkout management
- **usercred.db**: User authentication and access control

## Database Schema

### library.db

#### Books Table
```
book_id (INTEGER PRIMARY KEY)
title (TEXT)
author (TEXT)
genre (TEXT)
isbn (TEXT UNIQUE)
publication_year (INTEGER)
copies_available (INTEGER)
created_at (TIMESTAMP)
```

#### Patrons Table
```
patron_id (INTEGER PRIMARY KEY)
name (TEXT)
email (TEXT UNIQUE)
phone (TEXT)
address (TEXT)
membership_status (TEXT)
joined_date (TIMESTAMP)
```

#### Checkouts Table
```
checkout_id (INTEGER PRIMARY KEY)
patron_id (INTEGER FOREIGN KEY)
book_id (INTEGER FOREIGN KEY)
checkout_date (DATE)
due_date (DATE)
return_date (DATE)
fee (REAL)
status (TEXT - 'Active' or 'Returned')
```

### usercred.db

#### Users Table
```
user_id (INTEGER PRIMARY KEY)
username (TEXT UNIQUE)
password (TEXT - SHA256 hashed)
is_admin (INTEGER - 0 or 1)
created_at (TIMESTAMP)
last_login (TIMESTAMP)
```

## User Roles & Permissions

### 🔴 Admin User
**Credentials:** `admin` / `admin123`

**Permissions:**
- ✅ Add/Update/Delete Books
- ✅ Search Books
- ✅ Manage Users
- ✅ Manage Patrons
- ✅ Checkout/Return Books
- ✅ View Reports & Statistics
- ✅ View Overdue Books

### 🟠 Librarian User
**Credentials:** `librarian` / `librarian123`

**Permissions:**
- ✅ Add/Update/Delete Books
- ✅ Search Books
- ✅ Manage Patrons
- ✅ Checkout/Return Books
- ✅ View Reports & Statistics
- ✅ View Overdue Books
- ❌ Manage Users

### 🟡 Regular User
**Credentials:** `user1` / `user123` or `user2` / `user456`

**Permissions:**
- ✅ Search Books
- ✅ Checkout/Return Books
- ❌ Add/Update/Delete Books
- ❌ Manage Patrons
- ❌ View Reports
- ❌ Manage Users

## Running the Application

### Start the Library System
```bash
python3 library_system.py
```

### Login
```
🔐 LOGIN
Username: admin
Password: admin123
```

## Features

### 📚 Book Management
1. **Search Books** - Search by title, author, genre, or ISBN
2. **Add Book** - Add new books to the library (Admin/Librarian only)
3. **Update Book** - Modify book information (Admin/Librarian only)
4. **Delete Book** - Remove books from system (Admin/Librarian only)
5. **View All Books** - List all books with availability status

### 👥 Patron Management
1. **Add Patron** - Register new library members (Admin/Librarian only)
2. **View Patrons** - List all registered members (Admin/Librarian only)
3. **Search Patrons** - Search by name, email, or phone (Admin/Librarian only)

### 📋 Checkout & Return System
1. **Checkout Book** - Check out a book to a patron (14-day default)
2. **Return Book** - Process book return with automatic fine calculation
3. **View Active Checkouts** - List all books currently checked out
4. **View Overdue Books** - List books past due date (Reports only)

### 📊 Reports & Statistics
1. **Active Checkouts** - Current loans with due dates
2. **Overdue Books** - Books past due with days overdue
3. **All Books** - Complete library inventory

## Sample Data

### Books (5 pre-loaded)
| ID | Title | Author | Copies |
|----|-------|--------|--------|
| 1 | The Great Gatsby | F. Scott Fitzgerald | 3 |
| 2 | 1984 | George Orwell | 2 |
| 3 | To Kill a Mockingbird | Harper Lee | 2 |
| 4 | Pride and Prejudice | Jane Austen | 1 |
| 5 | The Catcher in the Rye | J.D. Salinger | 2 |

### Patrons (4 pre-loaded)
| ID | Name | Email |
|----|------|-------|
| 1 | Alice Johnson | alice@email.com |
| 2 | Bob Smith | bob@email.com |
| 3 | Carol White | carol@email.com |
| 4 | David Brown | david@email.com |

### Users
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| librarian | librarian123 | Librarian |
| user1 | user123 | Regular User |
| user2 | user456 | Regular User |

## Technical Details

### Security
- Passwords are hashed using SHA-256
- Role-based access control (RBAC) implemented
- Permission checking on all operations

### Classes & Architecture
```
AuthenticationManager
  ├── authenticate(username, password)
  ├── logout()
  └── is_authenticated()

User (Abstract)
  ├── AdminUser
  ├── LibrarianUser
  └── RegularUser

LibraryDatabase
  ├── connect()
  ├── execute(query, params)
  └── fetch(query, params)

UserDatabase
  ├── connect()
  ├── execute(query, params)
  └── fetch(query, params)

LibraryManager
  ├── Book Operations (add, delete, update, search)
  ├── Patron Operations (add, search, view)
  ├── Checkout Operations (checkout, return)
  └── Report Operations (overdue, active)
```

### Fine Calculation
- Late fee: $0.50 per day after due date
- Automatically calculated on book return
- Applied per checkout transaction

## File Structure
```
/workspaces/database-library/
├── library.db              # Main library database
├── usercred.db            # User credentials database
└── library_system.py      # Main application
```

## Usage Examples

### Example 1: Admin Adding a Book
```
Select option: 2
📖 ADD BOOK
Title: Python Crash Course
Author: Eric Matthes
Genre: Programming
ISBN: 978-1593279288
Publication Year: 2019
Number of Copies: 3
✓ Book added successfully
```

### Example 2: User Checking Out a Book
```
Select option: 5
Patron ID: 1
Book ID: 2
✓ Book checked out. Due date: 2025-12-23
```

### Example 3: User Returning a Book with Late Fee
```
Select option: 6
Checkout ID: 1
✓ Book returned successfully (Late fee: $2.50)
```

## Future Enhancements
- Web-based interface
- Email notifications for due dates
- Book reservations
- Renewal functionality
- Fine payment tracking
- Advanced reporting (circulation statistics)
- Multi-branch support
- ISBN barcode scanning

## License
Educational project for library management demonstration.

---
**Created:** December 2025
**Status:** Fully Functional
