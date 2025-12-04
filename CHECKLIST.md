# ✅ Setup & Test Checklist

## Pre-Flight Check

Run through this checklist to ensure everything is ready:

### ☐ Step 1: Verify Python Installation
```bash
python3 --version
# Should show Python 3.7 or higher
```

### ☐ Step 2: Install Dependencies
```bash
pip install mysql-connector-python
# or
pip install -r requirements.txt
```

### ☐ Step 3: Check MySQL Status
```bash
sudo service mysql status
# If not running:
sudo service mysql start
```

### ☐ Step 4: Configure Database Connection
```bash
# Copy example config
cp config.ini.example config.ini

# Edit with your MySQL password
nano config.ini
# or
code config.ini
```

Your `config.ini` should look like:
```ini
[database]
host = localhost
user = root
password = YOUR_ACTUAL_PASSWORD
database = librarydb
```

### ☐ Step 5: Import Database Schema
```bash
mysql -u root -p < schema.sql
# Enter your MySQL password when prompted
```

This creates:
- librarydb database
- 8 tables (authors, books, book_copies, etc.)
- 2 views (vw_books_complete, vw_active_transactions)
- Sample data (11 books, 10 authors, 5 members)

---

## 🧪 Run Tests

Now test everything in order:

### Test 1: Quick Test (Minimal)
```bash
python3 quick_test.py
```

**What it checks:**
- ✓ Python modules installed
- ✓ Files present
- ✓ MySQL connection works
- ✓ Database and tables exist

**Expected output:**
```
============================================================
MINIMAL CONNECTION TEST
============================================================

1. Testing imports...
   ✓ mysql.connector available

2. Checking files...
   ✓ config.ini found
   ✓ database.py found
   ✓ schema.sql found
   ✓ test_database.py found

3. Testing database module...
   ✓ DatabaseConnection class loaded
   ✓ DatabaseConnection initialized

4. Testing MySQL connection...
   ✓ Connected to MySQL!
   ✓ Database 'librarydb' exists
   ✓ Found 10 tables:
     - authors
     - book_authors
     - book_copies
     - book_genres
     - books
     ... and 5 more
   ✓ Disconnected

============================================================
Test complete!
============================================================
```

### Test 2: Connection Test (Detailed)
```bash
python3 test_connection.py
```

**What it checks:**
- Everything from quick_test.py
- MySQL version
- Table count validation
- Configuration validation

### Test 3: Full Test Suite (Comprehensive)
```bash
python3 test_database.py
```

**What it tests:**
- All CRUD operations
- Book management (add, search, update, delete)
- Member management
- Transaction flow (borrow, return, fines)
- Normalized relationships (many-to-many)
- Business logic (fine calculation)
- Database statistics

**Expected duration:** ~30 seconds

---

## 🐛 Troubleshooting

### Error: "No module named 'mysql'"
**Fix:**
```bash
pip install mysql-connector-python
```

### Error: "Can't connect to MySQL server"
**Check:**
```bash
# Is MySQL running?
sudo service mysql status

# Start it if not
sudo service mysql start

# Can you connect manually?
mysql -u root -p
```

### Error: "Access denied for user 'root'"
**Fix:**
```bash
# Edit config.ini with correct password
nano config.ini

# Or reset MySQL password if forgotten
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newpassword';
FLUSH PRIVILEGES;
EXIT;
```

### Error: "Unknown database 'librarydb'"
**Fix:**
```bash
# Import the schema
mysql -u root -p < schema.sql
```

### Error: "Table 'books' doesn't exist"
**Fix:**
```bash
# Re-import schema (drops and recreates)
mysql -u root -p < schema.sql
```

---

## 🎯 Quick Command Reference

### One-Line Full Setup
```bash
pip install mysql-connector-python && cp config.ini.example config.ini && echo "Edit config.ini now!" && mysql -u root -p < schema.sql && python3 quick_test.py
```

### Reset Database
```bash
mysql -u root -p < schema.sql
```

### Test Everything
```bash
python3 quick_test.py && python3 test_connection.py && python3 test_database.py
```

### Check What's in Database
```bash
mysql -u root -p librarydb -e "SHOW TABLES;"
mysql -u root -p librarydb -e "SELECT COUNT(*) FROM books;"
mysql -u root -p librarydb -e "SELECT * FROM vw_books_complete LIMIT 5;"
```

---

## ✨ Success Indicators

You'll know everything is working when:

1. ✅ `quick_test.py` shows all green checkmarks
2. ✅ `test_connection.py` says "ALL TESTS PASSED"
3. ✅ `test_database.py` completes without errors
4. ✅ You see book data in the output
5. ✅ Transaction tests show borrowing and returning works
6. ✅ Fine calculations are correct

---

## 📊 What's Next?

After all tests pass:

1. **Review the design**: Open `DATABASE_DESIGN.md`
2. **Try the GUI**: Run `python3 library_app_new.py`
3. **Read documentation**: Check `README.md`
4. **Prepare submission**: See `SUBMISSION_GUIDE.md`

---

## 🎓 For Your Assignment

When demonstrating to your instructor:

1. Show this checklist - proves you tested everything
2. Run `python3 test_database.py` - live demo
3. Show `DATABASE_DESIGN.md` - your design work
4. Explain `schema.sql` - your implementation
5. Walk through `database.py` - your business logic

Good luck! 🚀
