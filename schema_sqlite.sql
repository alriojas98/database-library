-- SQLite version of the Library Management System schema

-- Drop existing tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS book_copies;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;

-- Members table
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    member_type TEXT DEFAULT 'Standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books table
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    genres TEXT,
    isbn TEXT UNIQUE,
    publication_year INTEGER,
    pages INTEGER,
    description TEXT,
    publisher TEXT,
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book copies table (physical copies)
CREATE TABLE book_copies (
    copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Transactions table (borrowing records)
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    copy_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(8, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
);

-- Authors table (for reference)
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sample data
INSERT INTO members (name, email, member_type) VALUES
('John Doe', 'john.doe@email.com', 'Premium'),
('Jane Smith', 'jane.smith@email.com', 'Standard'),
('Bob Johnson', 'bob.johnson@email.com', 'Student'),
('Charlie Brown', 'charlie.brown@email.com', 'Premium'),
('Emily Davis', 'emily.davis@email.com', 'Premium');

INSERT INTO books (title, authors, genres, isbn, publication_year, pages, description, publisher, total_copies, available_copies) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Classic Literature, Fiction', '978-0446310789', 1960, 324, 'A novel about racial injustice in the American South', 'Penguin Random House', 3, 3),
('1984', 'George Orwell', 'Classic Literature, Dystopian', '978-0451524935', 1949, 328, 'Dystopian social science fiction novel', 'HarperCollins', 2, 2),
('Brave New World', 'Aldous Huxley', 'Dystopian, Science Fiction', '978-0060850524', 1932, 268, 'Dystopian novel about a futuristic society', 'HarperCollins', 2, 2),
('Jane Eyre', 'Charlotte Brontë', 'Classic Literature, Gothic Fiction', '978-0141441146', 1847, 532, 'Gothic romance novel', 'Penguin Random House', 2, 2),
('Murder on the Orient Express', 'Agatha Christie', 'Classic Literature, Mystery', '978-0062693662', 1934, 256, 'Classic detective mystery novel', 'HarperCollins', 2, 2),
('Pride and Prejudice', 'Jane Austen', 'Classic Literature, Romance', '978-0141439518', 1813, 432, 'A romantic novel of manners', 'Penguin Random House', 3, 3),
('The Catcher in the Rye', 'J.D. Salinger', 'Classic Literature, Fiction', '978-0316769488', 1951, 277, 'Novel about teenage rebellion and alienation', 'HarperCollins', 2, 2),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic Literature, Fiction', '978-0743273565', 1925, 180, 'A novel about the American Dream in the Jazz Age', 'Simon & Schuster', 2, 2),
('The Hobbit', 'J.R.R. Tolkien', 'Classic Literature, Fantasy', '978-0547928227', 1937, 310, 'Fantasy adventure novel', 'Hachette Book Group', 3, 3),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Classic Literature, Fantasy', '978-0618640157', 1954, 1178, 'Epic fantasy adventure trilogy', 'Hachette Book Group', 3, 3),
('To the Lighthouse', 'Virginia Woolf', 'Classic Literature, Fiction', '978-0156907392', 1927, 209, 'Modernist novel exploring consciousness', 'Macmillan Publishers', 1, 1);

-- Create book copies for each book
INSERT INTO book_copies (book_id, status) VALUES 
(1, 'Available'), (1, 'Available'), (1, 'Available'),
(2, 'Available'), (2, 'Available'),
(3, 'Available'), (3, 'Available'),
(4, 'Available'), (4, 'Available'),
(5, 'Available'), (5, 'Available'),
(6, 'Available'), (6, 'Available'), (6, 'Available'),
(7, 'Available'), (7, 'Available'),
(8, 'Available'), (8, 'Available'),
(9, 'Available'), (9, 'Available'), (9, 'Available'),
(10, 'Available'), (10, 'Available'), (10, 'Available'),
(11, 'Available');

-- Create indexes for better performance
CREATE INDEX idx_book_title ON books(title);
CREATE INDEX idx_book_isbn ON books(isbn);
CREATE INDEX idx_member_email ON members(email);
CREATE INDEX idx_copy_status ON book_copies(status);
CREATE INDEX idx_transaction_member ON transactions(member_id);
CREATE INDEX idx_transaction_copy ON transactions(copy_id);
