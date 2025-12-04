# 📊 Visual Guide - Library Database Schema

## Entity-Relationship Diagram (Detailed)

### Core Entities

```
┌─────────────────────────────────────────────┐
│              PUBLISHERS                      │
├─────────────────────────────────────────────┤
│ PK  publisher_id   INT                      │
│     name           VARCHAR(255) UNIQUE      │
│     country        VARCHAR(100)             │
│     website        VARCHAR(255)             │
│     created_at     TIMESTAMP                │
└─────────────────────────────────────────────┘
                    │
                    │ 1
                    │
                    │ Many
                    ▼
┌─────────────────────────────────────────────┐
│                 BOOKS                        │
├─────────────────────────────────────────────┤
│ PK  book_id          INT                    │
│     title            VARCHAR(255)           │
│     isbn             VARCHAR(20) UNIQUE     │
│     publication_year INT                    │
│ FK  publisher_id     INT                    │
│     language         VARCHAR(50)            │
│     pages            INT                    │
│     description      TEXT                   │
│     created_at       TIMESTAMP              │
└─────────────────────────────────────────────┘
       │                          │
       │ 1                    1   │
       │                          │
       │ Many                Many │
       ▼                          ▼
┌──────────────────┐      ┌──────────────────┐
│  BOOK_AUTHORS    │      │  BOOK_GENRES     │
├──────────────────┤      ├──────────────────┤
│ PK,FK book_id    │      │ PK,FK book_id    │
│ PK,FK author_id  │      │ PK,FK genre_id   │
│       author_ord │      └──────────────────┘
└──────────────────┘              │
       │                          │ Many
       │ Many                     │
       │                          │ 1
       ▼                          ▼
┌─────────────────────────────────────────────┐
│               AUTHORS                        │
├─────────────────────────────────────────────┤
│ PK  author_id     INT                       │
│     first_name    VARCHAR(100)              │
│     last_name     VARCHAR(100)              │
│     bio           TEXT                      │
│     birth_year    INT                       │
│     created_at    TIMESTAMP                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                GENRES                        │
├─────────────────────────────────────────────┤
│ PK  genre_id      INT                       │
│     name          VARCHAR(100) UNIQUE       │
│     description   TEXT                      │
│     created_at    TIMESTAMP                 │
└─────────────────────────────────────────────┘
```

### Transaction Flow

```
┌─────────────────────────────────────────────┐
│               MEMBERS                        │
├─────────────────────────────────────────────┤
│ PK  member_id        INT                    │
│     first_name       VARCHAR(100)           │
│     last_name        VARCHAR(100)           │
│     email            VARCHAR(255) UNIQUE    │
│     phone            VARCHAR(20)            │
│     address          TEXT                   │
│     join_date        DATE                   │
│     membership_type  ENUM('Standard',...)   │
│     status           ENUM('Active',...)     │
│     created_at       TIMESTAMP              │
└─────────────────────────────────────────────┘
                    │
                    │ 1
                    │
                    │ Many
                    ▼
┌─────────────────────────────────────────────┐
│             TRANSACTIONS                     │
├─────────────────────────────────────────────┤
│ PK  transaction_id  INT                     │
│ FK  member_id       INT                     │
│ FK  copy_id         INT                     │
│     borrow_date     DATE                    │
│     due_date        DATE                    │
│     return_date     DATE (nullable)         │
│     fine_amount     DECIMAL(10,2)           │
│     status          ENUM('Active',...)      │
│     created_at      TIMESTAMP               │
└─────────────────────────────────────────────┘
                    ▲
                    │ Many
                    │
                    │ 1
                    │
┌─────────────────────────────────────────────┐
│             BOOK_COPIES                      │
├─────────────────────────────────────────────┤
│ PK  copy_id          INT                    │
│ FK  book_id          INT                    │
│     condition_status ENUM('New',...)        │
│     location         VARCHAR(100)           │
│     status           ENUM('Available',...)  │
│     acquisition_date DATE                   │
└─────────────────────────────────────────────┘
                    ▲
                    │ Many
                    │
                    │ 1
                    │
              (links to BOOKS above)
```

---

## 🔗 Relationship Summary

### Many-to-Many Relationships

1. **BOOKS ↔ AUTHORS** (via BOOK_AUTHORS)
   - One book can have multiple authors (e.g., co-authors)
   - One author can write multiple books
   - Junction table tracks author order (primary vs. co-author)

2. **BOOKS ↔ GENRES** (via BOOK_GENRES)
   - One book can belong to multiple genres (e.g., "Science Fiction" + "Dystopian")
   - One genre contains multiple books
   - Junction table enables flexible categorization

### One-to-Many Relationships

3. **PUBLISHERS → BOOKS**
   - One publisher publishes many books
   - Each book has exactly one publisher

4. **BOOKS → BOOK_COPIES**
   - One book (title) can have multiple physical copies
   - Each copy belongs to exactly one book
   - Enables tracking individual items

5. **MEMBERS → TRANSACTIONS**
   - One member can have multiple borrowing transactions
   - Each transaction belongs to one member
   - Tracks borrowing history

6. **BOOK_COPIES → TRANSACTIONS**
   - One copy can be borrowed multiple times (over time)
   - Each transaction involves one specific copy
   - Maintains physical item tracking

---

## 📋 Table Relationships Matrix

| Table         | Relates To    | Type          | Via               |
|---------------|---------------|---------------|-------------------|
| books         | publishers    | Many-to-One   | FK publisher_id   |
| books         | authors       | Many-to-Many  | book_authors      |
| books         | genres        | Many-to-Many  | book_genres       |
| books         | book_copies   | One-to-Many   | FK book_id        |
| book_copies   | transactions  | One-to-Many   | FK copy_id        |
| members       | transactions  | One-to-Many   | FK member_id      |

---

## 🎯 Normalization Visual Example

### ❌ Before Normalization (Not 3NF)

```
BOOKS_UNNORMALIZED
┌──────────┬─────────────┬──────────────────┬────────────┬───────────────┐
│ book_id  │ title       │ authors          │ genres     │ publisher_name│
├──────────┼─────────────┼──────────────────┼────────────┼───────────────┤
│ 1        │ The Hobbit  │ J.R.R. Tolkien   │ Fantasy    │ Houghton Miff.│
│ 2        │ LOTR        │ J.R.R. Tolkien   │ Fantasy    │ Houghton Miff.│
│ 3        │ 1984        │ George Orwell    │ Dystopian  │ Penguin       │
└──────────┴─────────────┴──────────────────┴────────────┴───────────────┘

Problems:
- Redundancy: "J.R.R. Tolkien" stored multiple times
- Update anomaly: If author name changes, update multiple rows
- Insertion anomaly: Can't add author without a book
- Deletion anomaly: Deleting last book removes author info
```

### ✅ After Normalization (3NF)

```
AUTHORS                          BOOKS                     BOOK_AUTHORS
┌──────┬──────────────┐         ┌──────┬────────┐        ┌──────┬─────────┐
│ id   │ name         │         │ id   │ title  │        │book  │ author  │
├──────┼──────────────┤         ├──────┼────────┤        ├──────┼─────────┤
│ 1    │ J.R.R. Tolk. │    ┌───│ 1    │ Hobbit │────┐   │ 1    │ 1       │
│ 2    │ George Orw.  │    │   │ 2    │ LOTR   │    └──▶│ 2    │ 1       │
└──────┴──────────────┘    │   │ 3    │ 1984   │────────│ 3    │ 2       │
                            │   └──────┴────────┘        └──────┴─────────┘
PUBLISHERS                  │
┌──────┬──────────────┐    │
│ id   │ name         │    │
├──────┼──────────────┤    │
│ 1    │ Houghton M.  │◄───┘
│ 2    │ Penguin      │
└──────┴──────────────┘

Benefits:
✓ No redundancy: Each author stored once
✓ Easy updates: Change author name in one place
✓ Can add authors independently
✓ Data integrity maintained
```

---

## 🔄 Transaction Lifecycle

### Borrowing a Book

```
1. User Request
   ┌─────────────────┐
   │ Member wants to │
   │ borrow book #5  │
   └────────┬────────┘
            │
            ▼
2. Check Availability
   ┌─────────────────────────────┐
   │ SELECT copy_id              │
   │ FROM book_copies            │
   │ WHERE book_id = 5           │
   │   AND status = 'Available'  │
   └────────┬────────────────────┘
            │
            ▼
3. Create Transaction
   ┌─────────────────────────────┐
   │ INSERT INTO transactions    │
   │ (member_id, copy_id,        │
   │  borrow_date, due_date)     │
   └────────┬────────────────────┘
            │
            ▼
4. Update Copy Status
   ┌─────────────────────────────┐
   │ UPDATE book_copies          │
   │ SET status = 'Borrowed'     │
   │ WHERE copy_id = X           │
   └─────────────────────────────┘
```

### Returning a Book

```
1. Return Request
   ┌─────────────────┐
   │ Return trans.   │
   │ ID #123         │
   └────────┬────────┘
            │
            ▼
2. Calculate Fine
   ┌──────────────────────────────┐
   │ IF return_date > due_date    │
   │   fine = days_overdue * 0.50 │
   │ ELSE                         │
   │   fine = 0.00                │
   └────────┬─────────────────────┘
            │
            ▼
3. Update Transaction
   ┌──────────────────────────────┐
   │ UPDATE transactions          │
   │ SET return_date = TODAY,     │
   │     fine_amount = $X,        │
   │     status = 'Returned'      │
   └────────┬─────────────────────┘
            │
            ▼
4. Free Up Copy
   ┌──────────────────────────────┐
   │ UPDATE book_copies           │
   │ SET status = 'Available'     │
   └──────────────────────────────┘
```

---

## 📊 Sample Data Flow

### Adding a New Book with Authors and Genres

```
Input:
  Title: "The Silmarillion"
  Authors: ["J.R.R. Tolkien"]
  Genres: ["Fantasy", "Classic Literature"]
  Publisher: "Houghton Mifflin"

Processing:
  1. Get/Create Publisher ID
     ├─ Check if "Houghton Mifflin" exists
     └─ Use existing ID or create new

  2. Insert Book
     ├─ INSERT INTO books (title, publisher_id, ...)
     └─ Get new book_id = 12

  3. Link Authors
     ├─ Check if "J.R.R. Tolkien" exists → author_id = 5
     └─ INSERT INTO book_authors (12, 5, order=1)

  4. Link Genres
     ├─ Check if "Fantasy" exists → genre_id = 4
     ├─ INSERT INTO book_genres (12, 4)
     ├─ Check if "Classic Literature" exists → genre_id = 7
     └─ INSERT INTO book_genres (12, 7)

  5. Add Physical Copies
     ├─ INSERT INTO book_copies (book_id=12, status='Available')
     └─ INSERT INTO book_copies (book_id=12, status='Available')

Result:
  ✓ Book added with ID 12
  ✓ Linked to existing author (no duplication!)
  ✓ Linked to 2 genres
  ✓ 2 physical copies created
```

---

## 🎨 Three-Tier Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   TIER 3: Presentation                       │
│                     (User Interface)                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐        ┌─────────────────┐            │
│  │  library_app.py │   OR   │ test_database.py│            │
│  │  (Tkinter GUI)  │        │  (Test Suite)   │            │
│  └────────┬────────┘        └────────┬────────┘            │
└───────────┼──────────────────────────┼──────────────────────┘
            │                          │
            │  Function Calls          │
            ▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   TIER 2: Application                        │
│                    (Business Logic)                          │
├─────────────────────────────────────────────────────────────┤
│                    database.py                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ - get_all_books()                                    │   │
│  │ - search_books(term)                                 │   │
│  │ - add_book(title, author, ...)                       │   │
│  │ - borrow_book(member_id, book_id)                    │   │
│  │ - return_book(transaction_id)                        │   │
│  │ - calculate_fines()                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────┼──────────────────────────────────────────────────┘
            │
            │  SQL Queries
            ▼
┌─────────────────────────────────────────────────────────────┐
│                   TIER 1: Database                           │
│                    (Data Storage)                            │
├─────────────────────────────────────────────────────────────┤
│                    MySQL Server                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             librarydb Database                       │   │
│  │  ┌─────────────────────────────────────────┐        │   │
│  │  │  Tables:                                 │        │   │
│  │  │  • publishers                            │        │   │
│  │  │  • authors                               │        │   │
│  │  │  • books                                 │        │   │
│  │  │  • book_authors (junction)               │        │   │
│  │  │  • book_genres (junction)                │        │   │
│  │  │  • book_copies                           │        │   │
│  │  │  • members                               │        │   │
│  │  │  • transactions                          │        │   │
│  │  └─────────────────────────────────────────┘        │   │
│  │                                                      │   │
│  │  Views:                                              │   │
│  │  • vw_books_complete                                 │   │
│  │  • vw_active_transactions                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

Benefits of Three-Tier Architecture:
✓ Separation of Concerns: Each tier has distinct responsibility
✓ Maintainability: Changes in one tier don't affect others
✓ Scalability: Can scale tiers independently
✓ Security: Database credentials isolated in config
✓ Testability: Each layer can be tested independently
```

---

## 🎯 Index Strategy Visualization

```
Books Table (Without Indexes)
┌──────┬─────────────────────┬───────────────┬──────┐
│  ID  │        TITLE        │     ISBN      │ ...  │
├──────┼─────────────────────┼───────────────┼──────┤
│ 1    │ To Kill a Mocking.. │ 978-04463...  │      │  ← Linear scan
│ 2    │ 1984                │ 978-04515...  │      │  ← to find book
│ 3    │ Pride and Prejudice │ 978-01414...  │      │  ← by title
│ ...  │ ...                 │ ...           │      │  ← O(n) time
└──────┴─────────────────────┴───────────────┴──────┘

With Indexes:
┌──────────────────────────────────┐
│      idx_book_title (B-Tree)     │
├──────────────────────────────────┤
│ "1984" → row 2                   │  ← Fast lookup
│ "Pride..." → row 3               │  ← O(log n) time
│ "To Kill..." → row 1             │  ← Binary search
└──────────────────────────────────┘

Indexes Created:
✓ Primary Keys (automatic)
✓ Foreign Keys (for joins)
✓ title (for search)
✓ isbn (for unique lookups)
✓ author names (for author search)
✓ genre names (for filtering)
```

---

## 📈 Growth & Scalability

```
Initial State:
  Books: 11
  Copies: 26
  Members: 5
  Transactions: 6

After 1 Year:
  Books: ~500           ← Still efficient
  Copies: ~1,200        ← Indexes handle
  Members: ~200         ← Normalized design
  Transactions: ~5,000  ← scales well

After 5 Years:
  Books: ~2,000         ← No performance
  Copies: ~5,000        ← degradation
  Members: ~1,000       ← due to proper
  Transactions: ~50,000 ← indexing & 3NF
```

---

## 🔍 Query Performance Example

### Without Views (Complex Join)
```sql
-- User needs to see book with all details
SELECT b.title, a.first_name, a.last_name, 
       g.name, p.name, COUNT(bc.copy_id)
FROM books b
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
LEFT JOIN book_genres bg ON b.book_id = bg.book_id
LEFT JOIN genres g ON bg.genre_id = g.genre_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
LEFT JOIN book_copies bc ON b.book_id = bc.book_id
WHERE b.title LIKE '%Hobbit%'
GROUP BY b.book_id, ...;
-- Complex! Hard to write every time
```

### With Views (Simple Query)
```sql
-- Same result, much simpler
SELECT * FROM vw_books_complete
WHERE title LIKE '%Hobbit%';
-- Easy! Encapsulates complexity
```

---

This visual guide helps understand the complete database structure and how all pieces fit together! 📚✨
