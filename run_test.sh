#!/bin/bash
# Quick test script for Library Management System

echo "=================================================="
echo "Library Management System - Quick Test"
echo "=================================================="
echo ""

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    echo "   ✓ Python3 found: $(python3 --version)"
else
    echo "   ✗ Python3 not found!"
    exit 1
fi

# Check MySQL
echo ""
echo "2. Checking MySQL..."
if command -v mysql &> /dev/null; then
    echo "   ✓ MySQL client found: $(mysql --version)"
else
    echo "   ✗ MySQL client not found!"
    echo "   Install with: sudo apt-get install mysql-client"
fi

# Install Python dependencies
echo ""
echo "3. Installing Python dependencies..."
pip3 install mysql-connector-python --quiet
if [ $? -eq 0 ]; then
    echo "   ✓ Dependencies installed"
else
    echo "   ✗ Failed to install dependencies"
fi

# Check if database is accessible
echo ""
echo "4. Testing database connection..."
python3 << 'EOF'
import mysql.connector
try:
    # Try to connect
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password'  # Change this to your MySQL password
    )
    print("   ✓ MySQL server is accessible")
    conn.close()
except Exception as e:
    print(f"   ✗ Cannot connect to MySQL: {e}")
    print("   Make sure MySQL is running and config.ini has correct credentials")
EOF

# Import schema
echo ""
echo "5. Importing database schema..."
if command -v mysql &> /dev/null; then
    read -sp "   Enter MySQL root password: " MYSQL_PASS
    echo ""
    mysql -u root -p"$MYSQL_PASS" < schema.sql 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✓ Schema imported successfully"
    else
        echo "   ✗ Schema import failed"
    fi
else
    echo "   ⚠ MySQL client not available, skipping schema import"
    echo "   Run manually: mysql -u root -p < schema.sql"
fi

# Run test suite
echo ""
echo "6. Running test suite..."
python3 test_database.py

echo ""
echo "=================================================="
echo "Test complete!"
echo "=================================================="
