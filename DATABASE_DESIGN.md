# Library Management System - Database Design Documentation

## B.4: Relational Database Schema Design

### Problem Statement
Design and implement a comprehensive library management system that tracks books, members, borrowing transactions, authors, publishers, and genres. The system must support:
- Multiple authors per book
- Book copies and availability tracking
- Member borrowing history
- Fine calculations for overdue books
- Genre categorization
- Publisher information

---

## Conceptual Design (ER Model)

### Entities and Attributes

1. **Member**
   - member_id (PK)
   - first_name
   - last_name
   - email
   - phone
   - address
   - join_date
   - membership_type (Standard, Premium, Student)
   - status (Active, Suspended, Expired)

2. **Book**
   - book_id (PK)
   - title
   - isbn
   - publication_year
   - publisher_id (FK)
   - language
   - pages
   - description

3. **Author**
   - author_id (PK)
   - first_name
   - last_name
   - bio
   - birth_year

4. **Publisher**
   - publisher_id (PK)
   - name
   - country
   - website

5. **Genre**
   - genre_id (PK)
   - name
   - description

6. **BookCopy**
   - copy_id (PK)
   - book_id (FK)
   - condition (New, Good, Fair, Poor)
   - location (Shelf location)
   - status (Available, Borrowed, Reserved, Maintenance)

7. **Transaction**
   - transaction_id (PK)
   - member_id (FK)
   - copy_id (FK)
   - borrow_date
   - due_date
   - return_date
   - fine_amount
   - status (Active, Returned, Overdue)

### Relationships

1. **Book_Author** (Many-to-Many)
   - A book can have multiple authors
   - An author can write multiple books
   - book_id (FK), author_id (FK)

2. **Book_Genre** (Many-to-Many)
   - A book can belong to multiple genres
   - A genre can contain multiple books
   - book_id (FK), genre_id (FK)

3. **Book - Publisher** (Many-to-One)
   - A book has one publisher
   - A publisher publishes many books

4. **Book - BookCopy** (One-to-Many)
   - A book can have multiple physical copies
   - Each copy belongs to one book

5. **Member - Transaction** (One-to-Many)
   - A member can have multiple transactions
   - Each transaction belongs to one member

6. **BookCopy - Transaction** (One-to-Many)
   - A book copy can be borrowed multiple times
   - Each transaction involves one copy

### ER Diagram (Text Representation)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   MEMBER    │         │ TRANSACTION │         │  BOOKCOPY   │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ member_id PK│────┐    │transaction_i│    ┌────│ copy_id PK  │
│ first_name  │    │    │   d PK      │    │    │ book_id FK  │
│ last_name   │    │    │ member_id FK│◄───┘    │ condition   │
│ email       │    └───►│ copy_id FK  │────────►│ location    │
│ phone       │         │ borrow_date │         │ status      │
│ address     │         │ due_date    │         └──────┬──────┘
│ join_date   │         │ return_date │                │
│membership_ty│         │ fine_amount │                │
│ status      │         │ status      │                │
└─────────────┘         └─────────────┘                │
                                                        │
┌─────────────┐         ┌─────────────┐         ┌──────▼──────┐
│   AUTHOR    │         │ BOOK_AUTHOR │         │    BOOK     │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ author_id PK│◄────────│ book_id FK  │────────►│ book_id PK  │
│ first_name  │         │ author_id FK│         │ title       │
│ last_name   │         └─────────────┘         │ isbn        │
│ bio         │                                 │publication_y│
│ birth_year  │         ┌─────────────┐         │publisher_id │◄──┐
└─────────────┘         │ BOOK_GENRE  │         │ language    │   │
                        ├─────────────┤         │ pages       │   │
┌─────────────┐         │ book_id FK  │◄────────│ description │   │
│   GENRE     │         │ genre_id FK │         └─────────────┘   │
├─────────────┤         └─────────────┘                           │
│ genre_id PK │◄────────────────┘                                 │
│ name        │                                          ┌─────────┴───┐
│ description │                                          │  PUBLISHER  │
└─────────────┘                                          ├─────────────┤
                                                         │publisher_id │
                                                         │ name        │
                                                         │ country     │
                                                         │ website     │
                                                         └─────────────┘
```

---

## C.6: Normalization and Implementation

### Step 1: Normalization Analysis

#### First Normal Form (1NF)
**Requirement**: All attributes must contain atomic values; no repeating groups.

**Analysis**:
- ✓ All tables have atomic attributes
- ✓ No multi-valued attributes (e.g., authors are stored in separate junction table)
- ✓ Each row has a unique identifier (primary key)

#### Second Normal Form (2NF)
**Requirement**: Must be in 1NF and all non-key attributes must be fully dependent on the entire primary key.

**Analysis**:
- ✓ All single-attribute primary keys automatically satisfy 2NF
- ✓ Junction tables (Book_Author, Book_Genre) have composite keys where both attributes are needed to identify relationship
- ✓ No partial dependencies exist

#### Third Normal Form (3NF)
**Requirement**: Must be in 2NF and have no transitive dependencies (non-key attributes depend only on primary key).

**Analysis**:
- ✓ **Book-Publisher separation**: Publisher information extracted to separate table to avoid redundancy
- ✓ **Genre normalization**: Genre details stored separately, not repeated for each book
- ✓ **Author normalization**: Author information independent of books
- ✓ **BookCopy separation**: Physical copies separated from book metadata to track individual items
- ✓ No transitive dependencies: e.g., member_name → email → phone is avoided by direct relationships

**Normalization Benefits**:
1. **Reduced redundancy**: Publisher info stored once, referenced by many books
2. **Data integrity**: Author changes affect only Author table
3. **Flexibility**: Easy to add new genres, authors, or publishers
4. **Consistency**: ISBN uniqueness enforced at book level

---

### Step 2: Physical Schema Design

#### Indexing Strategy
1. **Primary Keys**: Auto-indexed for uniqueness
2. **Foreign Keys**: Indexed for join performance
3. **Search Fields**: title, author names, ISBN for frequent queries
4. **Composite Index**: (member_id, borrow_date) for transaction history

#### Constraints
1. **Primary Keys**: Ensure entity uniqueness
2. **Foreign Keys**: Maintain referential integrity with CASCADE rules
3. **Check Constraints**: Validate dates (return_date >= borrow_date)
4. **Unique Constraints**: ISBN uniqueness per book
5. **Default Values**: timestamps, status fields

---

### Step 3: Three-Tiered Architecture

#### Tier 1: Database Server (MySQL)
- Handles data storage and retrieval
- Enforces constraints and relationships
- Executes stored procedures and triggers
- Manages transactions and concurrency

#### Tier 2: Application Server (Python - database.py)
- Business logic implementation
- Data validation and sanitization
- Connection pooling
- Query execution and result processing
- Error handling and logging

#### Tier 3: Browser/Interface (Tkinter - library_app.py)
- User interface presentation
- Input collection and validation
- Result display and formatting
- User interaction handling

**Benefits**:
- **Separation of concerns**: Each tier has distinct responsibility
- **Maintainability**: Changes in one tier don't affect others
- **Scalability**: Can scale database and app servers independently
- **Security**: Database credentials isolated in config file
- **Testability**: Each layer can be tested independently

---

## Implementation Summary

The database design follows industry best practices:

1. **Comprehensive ER modeling** captures all entities and relationships
2. **Normalization to 3NF** eliminates redundancy and ensures data integrity
3. **Three-tiered architecture** provides separation, scalability, and maintainability
4. **Proper constraints and indexes** ensure performance and data quality
5. **Extensibility** allows easy addition of features (e.g., reservations, reviews)

This design satisfies competencies B.4 and C.6 by demonstrating complete database design from conceptual model through physical implementation in a multi-tiered application architecture.
