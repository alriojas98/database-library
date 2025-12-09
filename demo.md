# Library Management System - Quick Demo

## 🎯 What Was Created

### 1. **library.db** - Main Library Database
- **Books Table**: 5 classic books with availability tracking
- **Patrons Table**: 4 library members registered
- **Checkouts Table**: Transaction tracking with late fee calculation

### 2. **usercred.db** - User Authentication Database
- **Users Table**: 4 users with role-based access
- SHA-256 password hashing
- Login tracking with last_login timestamp

### 3. **library_system.py** - Complete Application
Role-based system with 3 user types and permission levels

## 🔐 Test Credentials

```
┌─────────────┬──────────────┬────────────────────────────┐
│ Username    │ Password     │ Role                       │
├─────────────┼──────────────┼────────────────────────────┤
│ admin       │ admin123     │ Admin (Full Access)        │
│ librarian   │ librarian123 │ Librarian (No User Mgmt)   │
│ user1       │ user123      │ Regular User (Limited)     │
│ user2       │ user456      │ Regular User (Limited)     │
└─────────────┴──────────────┴────────────────────────────┘
```

## 🚀 Quick Start

### Start the Application
```bash
cd /workspaces/database-library
python3 library_system.py
```

### Login as Admin
```
🔐 LOGIN
Username: admin
Password: admin123
✓ Welcome, admin!
```

## 📋 Available Operations

### For Admin/Librarian:
1. **Search Books** - Find books by title, author, genre, or ISBN
2. **Add Book** - Add new books to the library
3. **Update Book** - Modify book information
4. **Delete Book** - Remove books from system
5. **Add Patron** - Register new library members
6. **View Patrons** - List all members
7. **Search Patrons** - Find specific patrons

### For All Users:
5. **Checkout Book** - Check out a book (14 days default)
6. **Return Book** - Return a book (calculates late fees)
10. **View Active Checkouts** - See current loans
11. **View Overdue Books** (Admin/Librarian) - See past-due items
12. **View All Books** (Admin/Librarian) - Complete inventory

## 💰 Late Fee System
- **Fee Rate**: $0.50 per day overdue
- **Auto-calculated** on book return
- Example: 5 days late = $2.50 fee

## 🔑 Key Features

### 🛡️ Security
- SHA-256 password hashing
- Role-based access control
- Permission checking on all operations
- Login tracking

### 📊 Data Management
- Automatic copy availability tracking
- Transaction history
- Late fee calculations
- Patron and book search

### 📈 Reporting
- Active checkouts with due dates
- Overdue books with days late
- Complete book inventory
- Patron information

## 📁 Database Files

```
library.db (5 tables + relationships)
├── Books (5 pre-loaded)
├── Patrons (4 pre-loaded)
└── Checkouts (for transactions)

usercred.db (1 table)
└── Users (4 pre-loaded)
```

## ✨ Sample Workflow

### As Admin:
1. Login with admin credentials
2. Search for "1984"
3. Add a new book "Python Crash Course"
4. View all books
5. Check active checkouts
6. Return to main menu

### As Regular User:
1. Login with user1 credentials
2. Search for available books
3. Checkout "The Great Gatsby" (Patron ID: 1)
4. View active checkouts
5. Return the book
6. See automatic fine calculation if late

## 🔧 Technical Stack

- **Language**: Python 3
- **Database**: SQLite (2 separate databases)
- **Architecture**: Object-oriented with abstract base classes
- **Security**: SHA-256 hashing, RBAC
- **Design Pattern**: Role-based permissions

## 📝 Next Steps

Try these operations:

1. **Add a Book as Librarian**
   - Login: librarian / librarian123
   - Choose option 2 (Add Book)
   - Enter book details

2. **Checkout a Book as Regular User**
   - Login: user1 / user123
   - Choose option 5 (Checkout Book)
   - Patron ID: 1, Book ID: 2

3. **Return with Late Fee**
   - Choose option 6 (Return Book)
   - System auto-calculates fee if overdue

4. **View Reports as Admin**
   - Login: admin / admin123
   - Choose option 11 (View Overdue Books)
   - Choose option 12 (View All Books)

## 📚 Files Modified/Created

```
✅ library.db                   - New database
✅ usercred.db                  - New database
✅ library_system.py            - New application (900+ lines)
✅ LIBRARY_SYSTEM_README.md     - Documentation
✅ demo.md                      - This file
```

## 🎓 Educational Purpose

This system demonstrates:
- Database normalization (3NF)
- Role-based access control (RBAC)
- Object-oriented programming with inheritance
- Secure password handling
- Transaction management
- Business logic implementation
- CRUD operations
- User authentication

---
**Status**: ✅ Complete & Tested
**Last Updated**: December 2025
