#!/usr/bin/env python3
"""
Simple test to verify the database connection and basic functionality
Run this before the full test suite to ensure everything is set up correctly
"""

import sys

def test_imports():
    """Test if required modules can be imported"""
    print("Testing imports...")
    try:
        import mysql.connector
        print("✓ mysql.connector is installed")
        return True
    except ImportError:
        print("✗ mysql.connector not found")
        print("  Install with: pip install mysql-connector-python")
        return False

def test_config():
    """Test if config file exists"""
    print("\nTesting configuration...")
    try:
        import configparser
        import os
        
        if os.path.exists('config.ini'):
            print("✓ config.ini found")
            config = configparser.ConfigParser()
            config.read('config.ini')
            
            if 'database' in config:
                print(f"  Host: {config['database'].get('host', 'N/A')}")
                print(f"  User: {config['database'].get('user', 'N/A')}")
                print(f"  Database: {config['database'].get('database', 'N/A')}")
                return True
            else:
                print("✗ [database] section not found in config.ini")
                return False
        else:
            print("✗ config.ini not found")
            print("  Copy config.ini.example to config.ini and edit it")
            return False
    except Exception as e:
        print(f"✗ Error reading config: {e}")
        return False

def test_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from database import DatabaseConnection
        
        db = DatabaseConnection('config.ini')
        if db.connect():
            print("✓ Connected to MySQL successfully")
            
            # Try a simple query
            result = db.execute_query("SELECT VERSION()")
            if result:
                print(f"  MySQL version: {result[0][0]}")
            
            # Check if librarydb exists
            result = db.execute_query("SHOW DATABASES LIKE 'librarydb'")
            if result and len(result) > 0:
                print("✓ librarydb database exists")
            else:
                print("✗ librarydb database not found")
                print("  Import schema with: mysql -u root -p < schema.sql")
                db.disconnect()
                return False
            
            # Check if tables exist
            result = db.execute_query("USE librarydb; SHOW TABLES")
            if result and len(result) > 0:
                print(f"✓ Found {len(result)} tables")
            else:
                print("✗ No tables found in librarydb")
                db.disconnect()
                return False
            
            db.disconnect()
            print("✓ Disconnected successfully")
            return True
        else:
            print("✗ Could not connect to MySQL")
            print("  Check your credentials in config.ini")
            print("  Make sure MySQL is running")
            return False
            
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("  Library Management System - Quick Connectivity Test")
    print("="*60)
    print()
    
    results = []
    results.append(test_imports())
    results.append(test_config())
    results.append(test_connection())
    
    print("\n" + "="*60)
    if all(results):
        print("✓ ALL TESTS PASSED - Ready to run full test suite!")
        print("\nRun the full test suite with:")
        print("  python test_database.py")
    else:
        print("✗ SOME TESTS FAILED - Fix the issues above")
        print("\nSetup checklist:")
        print("  1. Install dependencies: pip install mysql-connector-python")
        print("  2. Configure database: cp config.ini.example config.ini")
        print("  3. Edit config.ini with your MySQL credentials")
        print("  4. Import schema: mysql -u root -p < schema.sql")
    print("="*60)
    print()
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
