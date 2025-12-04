# 🚀 Let's Run It! - Step by Step Guide

## Quick Test Steps

### Step 1: Test Connection First

Run the simple connection test to make sure everything is ready:

```bash
python test_connection.py
```

This will check:
- ✓ Python dependencies installed
- ✓ config.ini exists and is valid
- ✓ MySQL is accessible
- ✓ librarydb database exists
- ✓ Tables are created

### Step 2: If Connection Test Passes

Run the full test suite:

```bash
python test_database.py
```

---

## Setup Commands (If Needed)

### If MySQL is not installed:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server mysql-client

# Start MySQL
sudo service mysql start
```

### If Python dependencies are missing:

```bash
pip install mysql-connector-python
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### If config.ini doesn't exist:

```bash
cp config.ini.example config.ini
# Then edit config.ini with your MySQL password
nano config.ini
```

### If database needs to be created:

```bash
# Interactive (prompts for password)
mysql -u root -p < schema.sql

# Or non-interactive (if you know the password)
mysql -u root -pYourPassword < schema.sql
```

---

## Quick One-Liner Setup

If you want to do everything at once:

```bash
# Install deps, import schema, run test
pip install mysql-connector-python && \
mysql -u root -p < schema.sql && \
python test_database.py
```

---

## Troubleshooting

### Error: "Can't connect to MySQL server"
```bash
# Check if MySQL is running
sudo service mysql status

# If not running, start it
sudo service mysql start
```

### Error: "Access denied for user 'root'"
Edit `config.ini` with correct password:
```ini
[database]
password = your_actual_mysql_password
```

### Error: "No module named 'mysql.connector'"
```bash
pip install mysql-connector-python
```

### Error: "Unknown database 'librarydb'"
```bash
mysql -u root -p < schema.sql
```

---

## Expected Output

### Connection Test Success:
```
============================================================
  Library Management System - Quick Connectivity Test
============================================================

Testing imports...
✓ mysql.connector is installed

Testing configuration...
✓ config.ini found
  Host: localhost
  User: root
  Database: librarydb

Testing database connection...
✓ Connected to MySQL successfully
  MySQL version: 8.0.x
✓ librarydb database exists
✓ Found 10 tables
✓ Disconnected successfully

============================================================
✓ ALL TESTS PASSED - Ready to run full test suite!
============================================================
```

### Full Test Suite Success:
```
======================================================================
  LIBRARY MANAGEMENT SYSTEM - DATABASE TEST SUITE
======================================================================

✓ Database connection established successfully!

======================================================================
  1. BOOK OPERATIONS - Testing Normalized Schema
======================================================================

[1.1] Get All Books (from vw_books_complete view):
  Found 11 books
  
  Sample books:
    - 1984 by George Orwell
      Genres: Dystopian, Classic Literature | Copies: 2 available / 2 total
    ...

[1.4] Add New Book (with authors and genres):
  ✓ Successfully added book with ID: 12
  ✓ Automatically linked to author 'J.R.R. Tolkien'
  ✓ Automatically linked to genres: Fantasy, Classic Literature
  ✓ Created 2 physical copies

... (more test output) ...

======================================================================
  TEST SUITE COMPLETED
======================================================================

  ✓ All database operations tested successfully
  ✓ Normalized schema (3NF) validated
  ✓ Three-tiered architecture demonstrated
  ✓ Referential integrity maintained
  ✓ Business logic implemented correctly
```

---

## What Each Test Does

### test_connection.py (Quick Check)
- Verifies Python dependencies
- Checks config file
- Tests MySQL connection
- Verifies database and tables exist
- **Run time: ~5 seconds**

### test_database.py (Full Suite)
- Tests all CRUD operations
- Demonstrates normalized relationships
- Tests borrowing/returning books
- Calculates fines
- Shows database statistics
- **Run time: ~30 seconds**

---

## Ready to Go!

Just run:

```bash
python test_connection.py
```

If that passes, then run:

```bash
python test_database.py
```

🎉 You're all set!
