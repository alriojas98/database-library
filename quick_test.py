#!/usr/bin/env python3
"""
Minimal test - just check if we can import and connect
"""

print("="*60)
print("MINIMAL CONNECTION TEST")
print("="*60)

# Test 1: Import test
print("\n1. Testing imports...")
try:
    import mysql.connector
    print("   ✓ mysql.connector available")
except ImportError as e:
    print(f"   ✗ mysql.connector not found: {e}")
    print("   Run: pip install mysql-connector-python")
    exit(1)

# Test 2: Check files
print("\n2. Checking files...")
import os
files = ['config.ini', 'database.py', 'schema.sql', 'test_database.py']
for f in files:
    if os.path.exists(f):
        print(f"   ✓ {f} found")
    else:
        print(f"   ✗ {f} missing")

# Test 3: Try to load database module
print("\n3. Testing database module...")
try:
    from database import DatabaseConnection
    print("   ✓ DatabaseConnection class loaded")
    
    # Try to initialize (won't connect yet)
    db = DatabaseConnection('config.ini')
    print("   ✓ DatabaseConnection initialized")
    
except Exception as e:
    print(f"   ✗ Error loading database module: {e}")
    exit(1)

# Test 4: Try connection
print("\n4. Testing MySQL connection...")
try:
    if db.connect():
        print("   ✓ Connected to MySQL!")
        
        # Check database
        result = db.execute_query("SHOW DATABASES LIKE 'librarydb'")
        if result and len(result) > 0:
            print("   ✓ Database 'librarydb' exists")
            
            # Check tables
            db.execute_query("USE librarydb")
            result = db.execute_query("SHOW TABLES")
            if result:
                print(f"   ✓ Found {len(result)} tables:")
                for table in result[:5]:  # Show first 5
                    print(f"     - {table[0]}")
                if len(result) > 5:
                    print(f"     ... and {len(result) - 5} more")
            else:
                print("   ✗ No tables found")
        else:
            print("   ✗ Database 'librarydb' not found")
            print("   Run: mysql -u root -p < schema.sql")
        
        db.disconnect()
        print("   ✓ Disconnected")
        
    else:
        print("   ✗ Could not connect to MySQL")
        print("   Check:")
        print("     - MySQL is running: sudo service mysql status")
        print("     - config.ini has correct credentials")
        
except Exception as e:
    print(f"   ✗ Connection error: {e}")
    print("\n   Possible fixes:")
    print("   - Start MySQL: sudo service mysql start")
    print("   - Check config.ini password")
    print("   - Import schema: mysql -u root -p < schema.sql")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
