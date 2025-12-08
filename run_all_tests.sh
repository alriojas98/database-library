#!/bin/bash
# Simple test runner - tries all tests in order

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Library Management System - Test Runner               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Quick test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Quick Connection Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python quick_test.py
TEST1=$?

if [ $TEST1 -eq 0 ]; then
    echo -e "${GREEN}✓ Quick test passed${NC}"
    echo ""
    
    # Test 2: Connection test
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Test 2: Detailed Connection Test"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python test_connection.py
    TEST2=$?
    
    if [ $TEST2 -eq 0 ]; then
        echo -e "${GREEN}✓ Connection test passed${NC}"
        echo ""
        
        # Test 3: Full test suite
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Test 3: Full Test Suite (This may take 30 seconds...)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        python test_database.py
        TEST3=$?
        
        if [ $TEST3 -eq 0 ]; then
            echo ""
            echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║  ✓ ALL TESTS PASSED! System is working perfectly!     ║${NC}"
            echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
            echo ""
            echo "Next steps:"
            echo "  • Review DATABASE_DESIGN.md for your design documentation"
            echo "  • Check SUBMISSION_GUIDE.md for how to submit"
            echo "  • Try the GUI: python3 library_app_new.py"
        else
            echo -e "${RED}✗ Full test suite failed${NC}"
        fi
    else
        echo -e "${RED}✗ Connection test failed${NC}"
        echo "Fix connection issues before running full tests"
    fi
else
    echo -e "${RED}✗ Quick test failed${NC}"
    echo ""
    echo -e "${YELLOW}Common fixes:${NC}"
    echo "  1. Install dependencies: pip install mysql-connector-python"
    echo "  2. Start MySQL: sudo service mysql start"
    echo "  3. Configure: cp config.ini.example config.ini"
    echo "  4. Import schema: mysql -u root -p < schema.sql"
    echo ""
    echo "See CHECKLIST.md for detailed setup instructions"
fi

echo ""
