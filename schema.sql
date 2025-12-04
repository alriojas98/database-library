-- ============================================================================
-- Library Management System - Normalized Database Schema (3NF)
-- ============================================================================
-- This script implements a complete relational database design for a library
-- management system following normalization principles up to 3rd Normal Form.
--
-- Design Competencies Demonstrated:
-- - B.4: Conceptual/Logical/Physical database design from problem statement
-- - C.6: Three-stage implementation (ER design, normalization, 3-tier system)
-- ============================================================================

-- Drop existing database and recreate (for clean setup)
DROP DATABASE IF EXISTS librarydb;
CREATE DATABASE librarydb;
USE librarydb;

-- ============================================================================
-- ENTITY TABLES (3NF Normalized)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Publishers Table
-- Stores publisher information independently to avoid redundancy
-- ----------------------------------------------------------------------------
CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_publisher_name (name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Authors Table
-- Stores author information independently to support multiple authors per book
-- ----------------------------------------------------------------------------
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    bio TEXT,
    birth_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_author_name (last_name, first_name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Genres Table
-- Normalized genre information to avoid repetition and support multiple genres
-- ----------------------------------------------------------------------------
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_genre_name (name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Books Table
-- Core book metadata without redundant author/genre information
-- Foreign key to publisher maintains referential integrity
-- ----------------------------------------------------------------------------
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INT,
    publisher_id INT,
    language VARCHAR(50) DEFAULT 'English',
    pages INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    INDEX idx_book_title (title),
    INDEX idx_book_isbn (isbn),
    INDEX idx_book_publisher (publisher_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Book Copies Table
-- Separates physical copies from book metadata (allows multiple copies per book)
-- Tracks individual item status and location
-- ----------------------------------------------------------------------------
CREATE TABLE book_copies (
    copy_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    condition_status ENUM('New', 'Good', 'Fair', 'Poor') DEFAULT 'Good',
    location VARCHAR(100),
    status ENUM('Available', 'Borrowed', 'Reserved', 'Maintenance', 'Lost') DEFAULT 'Available',
    acquisition_date DATE DEFAULT (CURRENT_DATE),
    
    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    INDEX idx_copy_book (book_id),
    INDEX idx_copy_status (status)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Members Table
-- Library member information with membership type and status tracking
-- ----------------------------------------------------------------------------
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    join_date DATE DEFAULT (CURRENT_DATE),
    membership_type ENUM('Standard', 'Premium', 'Student') DEFAULT 'Standard',
    status ENUM('Active', 'Suspended', 'Expired') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_member_email (email),
    INDEX idx_member_name (last_name, first_name),
    INDEX idx_member_status (status)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Transactions Table
-- Tracks borrowing history with dates and fines
-- Links members to specific book copies
-- ----------------------------------------------------------------------------
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    copy_id INT NOT NULL,
    borrow_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('Active', 'Returned', 'Overdue') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (member_id) REFERENCES members(member_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    
    -- Ensure return date is after or equal to borrow date
    CONSTRAINT chk_return_after_borrow CHECK (return_date IS NULL OR return_date >= borrow_date),
    
    INDEX idx_transaction_member (member_id),
    INDEX idx_transaction_copy (copy_id),
    INDEX idx_transaction_dates (borrow_date, due_date),
    INDEX idx_transaction_status (status)
) ENGINE=InnoDB;

-- ============================================================================
-- JUNCTION TABLES (Many-to-Many Relationships)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Book_Authors Junction Table
-- Implements many-to-many relationship between books and authors
-- A book can have multiple authors, an author can write multiple books
-- ----------------------------------------------------------------------------
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    author_order INT DEFAULT 1,  -- For primary author vs. co-authors
    
    PRIMARY KEY (book_id, author_id),
    
    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    INDEX idx_ba_author (author_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Book_Genres Junction Table
-- Implements many-to-many relationship between books and genres
-- A book can belong to multiple genres, a genre can contain multiple books
-- ----------------------------------------------------------------------------
CREATE TABLE book_genres (
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    
    PRIMARY KEY (book_id, genre_id),
    
    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    INDEX idx_bg_genre (genre_id)
) ENGINE=InnoDB;

-- ============================================================================
-- VIEWS FOR SIMPLIFIED QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Complete Book Information View
-- Joins books with authors, genres, and publisher for easy querying
-- ----------------------------------------------------------------------------
CREATE VIEW vw_books_complete AS
SELECT 
    b.book_id,
    b.title,
    b.isbn,
    b.publication_year,
    b.language,
    b.pages,
    b.description,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) ORDER BY ba.author_order SEPARATOR ', ') AS authors,
    GROUP_CONCAT(DISTINCT g.name ORDER BY g.name SEPARATOR ', ') AS genres,
    p.name AS publisher,
    COUNT(DISTINCT bc.copy_id) AS total_copies,
    SUM(CASE WHEN bc.status = 'Available' THEN 1 ELSE 0 END) AS available_copies
FROM books b
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
LEFT JOIN book_genres bg ON b.book_id = bg.book_id
LEFT JOIN genres g ON bg.genre_id = g.genre_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
LEFT JOIN book_copies bc ON b.book_id = bc.book_id
GROUP BY b.book_id, b.title, b.isbn, b.publication_year, b.language, 
         b.pages, b.description, p.name;

-- ----------------------------------------------------------------------------
-- Active Transactions View
-- Shows current borrowed books with member and book details
-- ----------------------------------------------------------------------------
CREATE VIEW vw_active_transactions AS
SELECT 
    t.transaction_id,
    t.borrow_date,
    t.due_date,
    DATEDIFF(CURDATE(), t.due_date) AS days_overdue,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    m.email AS member_email,
    b.title AS book_title,
    CONCAT(a.first_name, ' ', a.last_name) AS author_name,
    bc.copy_id,
    t.status
FROM transactions t
JOIN members m ON t.member_id = m.member_id
JOIN book_copies bc ON t.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
LEFT JOIN book_authors ba ON b.book_id = ba.book_id AND ba.author_order = 1
LEFT JOIN authors a ON ba.author_id = a.author_id
WHERE t.status IN ('Active', 'Overdue')
ORDER BY t.due_date;

-- ============================================================================
-- SAMPLE DATA INSERTION
-- ============================================================================

-- Insert Publishers
INSERT INTO publishers (name, country, website) VALUES
('Penguin Random House', 'USA', 'https://www.penguinrandomhouse.com'),
('HarperCollins', 'USA', 'https://www.harpercollins.com'),
('Simon & Schuster', 'USA', 'https://www.simonandschuster.com'),
('Hachette Book Group', 'USA', 'https://www.hachettebookgroup.com'),
('Macmillan Publishers', 'UK', 'https://www.macmillan.com');

-- Insert Authors
INSERT INTO authors (first_name, last_name, bio, birth_year) VALUES
('Harper', 'Lee', 'American novelist best known for To Kill a Mockingbird', 1926),
('George', 'Orwell', 'English novelist and essayist, journalist and critic', 1903),
('Jane', 'Austen', 'English novelist known for her romantic fiction', 1775),
('F. Scott', 'Fitzgerald', 'American novelist of the Jazz Age', 1896),
('J.R.R.', 'Tolkien', 'English writer, philologist, and academic', 1892),
('J.D.', 'Salinger', 'American writer known for The Catcher in the Rye', 1919),
('Virginia', 'Woolf', 'English writer and modernist pioneer', 1882),
('Aldous', 'Huxley', 'English writer and philosopher', 1894),
('Charlotte', 'Brontë', 'English novelist and poet', 1816),
('Agatha', 'Christie', 'English writer of detective fiction', 1890);

-- Insert Genres
INSERT INTO genres (name, description) VALUES
('Fiction', 'Literary works based on imagination'),
('Dystopian', 'Fiction depicting oppressive societal control'),
('Romance', 'Fiction focused on romantic relationships'),
('Fantasy', 'Fiction involving magical or supernatural elements'),
('Gothic Fiction', 'Fiction combining romance and horror elements'),
('Mystery', 'Fiction dealing with puzzle-solving and crime'),
('Classic Literature', 'Enduring works of recognized literary merit'),
('Science Fiction', 'Fiction based on futuristic science and technology');

-- Insert Books
INSERT INTO books (title, isbn, publication_year, publisher_id, language, pages, description) VALUES
('To Kill a Mockingbird', '978-0446310789', 1960, 1, 'English', 324, 'A novel about racial injustice in the American South'),
('1984', '978-0451524935', 1949, 2, 'English', 328, 'Dystopian social science fiction novel'),
('Pride and Prejudice', '978-0141439518', 1813, 1, 'English', 432, 'A romantic novel of manners'),
('The Great Gatsby', '978-0743273565', 1925, 3, 'English', 180, 'A novel about the American Dream in the Jazz Age'),
('The Hobbit', '978-0547928227', 1937, 4, 'English', 310, 'Fantasy adventure novel'),
('The Catcher in the Rye', '978-0316769488', 1951, 2, 'English', 277, 'Novel about teenage rebellion and alienation'),
('To the Lighthouse', '978-0156907392', 1927, 5, 'English', 209, 'Modernist novel exploring consciousness'),
('Brave New World', '978-0060850524', 1932, 2, 'English', 268, 'Dystopian novel about a futuristic society'),
('The Lord of the Rings', '978-0618640157', 1954, 4, 'English', 1178, 'Epic fantasy adventure trilogy'),
('Jane Eyre', '978-0141441146', 1847, 1, 'English', 532, 'Gothic romance novel'),
('Murder on the Orient Express', '978-0062693662', 1934, 2, 'English', 256, 'Classic detective mystery novel');

-- Link Books to Authors
INSERT INTO book_authors (book_id, author_id, author_order) VALUES
(1, 1, 1),   -- To Kill a Mockingbird - Harper Lee
(2, 2, 1),   -- 1984 - George Orwell
(3, 3, 1),   -- Pride and Prejudice - Jane Austen
(4, 4, 1),   -- The Great Gatsby - F. Scott Fitzgerald
(5, 5, 1),   -- The Hobbit - J.R.R. Tolkien
(6, 6, 1),   -- The Catcher in the Rye - J.D. Salinger
(7, 7, 1),   -- To the Lighthouse - Virginia Woolf
(8, 8, 1),   -- Brave New World - Aldous Huxley
(9, 5, 1),   -- The Lord of the Rings - J.R.R. Tolkien
(10, 9, 1),  -- Jane Eyre - Charlotte Brontë
(11, 10, 1); -- Murder on the Orient Express - Agatha Christie

-- Link Books to Genres
INSERT INTO book_genres (book_id, genre_id) VALUES
(1, 1), (1, 7),    -- To Kill a Mockingbird: Fiction, Classic
(2, 2), (2, 7),    -- 1984: Dystopian, Classic
(3, 3), (3, 7),    -- Pride and Prejudice: Romance, Classic
(4, 1), (4, 7),    -- The Great Gatsby: Fiction, Classic
(5, 4), (5, 7),    -- The Hobbit: Fantasy, Classic
(6, 1), (6, 7),    -- The Catcher in the Rye: Fiction, Classic
(7, 1), (7, 7),    -- To the Lighthouse: Fiction, Classic
(8, 2), (8, 8),    -- Brave New World: Dystopian, Science Fiction
(9, 4), (9, 7),    -- The Lord of the Rings: Fantasy, Classic
(10, 5), (10, 7),  -- Jane Eyre: Gothic Fiction, Classic
(11, 6), (11, 7);  -- Murder on the Orient Express: Mystery, Classic

-- Insert Book Copies (2-3 copies per book)
INSERT INTO book_copies (book_id, condition_status, location, status) VALUES
-- To Kill a Mockingbird (3 copies)
(1, 'Good', 'A-101', 'Available'),
(1, 'Good', 'A-102', 'Available'),
(1, 'Fair', 'A-103', 'Available'),
-- 1984 (2 copies)
(2, 'New', 'A-201', 'Available'),
(2, 'Good', 'A-202', 'Available'),
-- Pride and Prejudice (3 copies)
(3, 'Good', 'B-101', 'Available'),
(3, 'Fair', 'B-102', 'Available'),
(3, 'Good', 'B-103', 'Available'),
-- The Great Gatsby (2 copies)
(4, 'New', 'C-101', 'Available'),
(4, 'Good', 'C-102', 'Available'),
-- The Hobbit (3 copies)
(5, 'Good', 'D-101', 'Available'),
(5, 'Good', 'D-102', 'Available'),
(5, 'New', 'D-103', 'Available'),
-- The Catcher in the Rye (2 copies)
(6, 'Good', 'E-101', 'Available'),
(6, 'Fair', 'E-102', 'Available'),
-- To the Lighthouse (2 copies)
(7, 'Good', 'F-101', 'Available'),
(7, 'Good', 'F-102', 'Available'),
-- Brave New World (2 copies)
(8, 'New', 'G-101', 'Available'),
(8, 'Good', 'G-102', 'Available'),
-- The Lord of the Rings (3 copies)
(9, 'Good', 'D-201', 'Available'),
(9, 'New', 'D-202', 'Available'),
(9, 'Good', 'D-203', 'Available'),
-- Jane Eyre (2 copies)
(10, 'Good', 'H-101', 'Available'),
(10, 'Fair', 'H-102', 'Available'),
-- Murder on the Orient Express (2 copies)
(11, 'New', 'I-101', 'Available'),
(11, 'Good', 'I-102', 'Available');

-- Insert Sample Members
INSERT INTO members (first_name, last_name, email, phone, address, membership_type, status) VALUES
('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St, City, State 12345', 'Premium', 'Active'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave, City, State 12345', 'Standard', 'Active'),
('Bob', 'Johnson', 'bob.johnson@email.com', '555-0103', '789 Pine Rd, City, State 12345', 'Student', 'Active'),
('Alice', 'Williams', 'alice.williams@email.com', '555-0104', '321 Elm St, City, State 12345', 'Standard', 'Active'),
('Charlie', 'Brown', 'charlie.brown@email.com', '555-0105', '654 Maple Dr, City, State 12345', 'Premium', 'Active');

-- Insert Sample Transactions (some active borrowing)
INSERT INTO transactions (member_id, copy_id, borrow_date, due_date, status) VALUES
(1, 1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'Active'),
(2, 4, DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'Active'),
(3, 11, DATE_SUB(CURDATE(), INTERVAL 7 DAY), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 'Active');

-- Update book copy status for borrowed books
UPDATE book_copies SET status = 'Borrowed' WHERE copy_id IN (1, 4, 11);

-- Insert some completed transactions (historical data)
INSERT INTO transactions (member_id, copy_id, borrow_date, due_date, return_date, status) VALUES
(1, 2, DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 20 DAY), 'Returned'),
(2, 5, DATE_SUB(CURDATE(), INTERVAL 25 DAY), DATE_SUB(CURDATE(), INTERVAL 11 DAY), DATE_SUB(CURDATE(), INTERVAL 12 DAY), 'Returned'),
(4, 8, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 6 DAY), DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'Returned');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Show complete book catalog with all information
SELECT * FROM vw_books_complete ORDER BY title;

-- Show active transactions
SELECT * FROM vw_active_transactions;

-- Summary statistics
SELECT 
    'Total Books' AS metric, COUNT(*) AS count FROM books
UNION ALL
SELECT 'Total Copies', COUNT(*) FROM book_copies
UNION ALL
SELECT 'Available Copies', COUNT(*) FROM book_copies WHERE status = 'Available'
UNION ALL
SELECT 'Total Members', COUNT(*) FROM members
UNION ALL
SELECT 'Active Transactions', COUNT(*) FROM transactions WHERE status = 'Active';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================