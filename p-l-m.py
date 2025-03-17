import sqlite3

# Database Connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER,
        genre TEXT,
        read_status BOOLEAN
    )
""")
conn.commit()

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, read_status))
    conn.commit()
    print("Book added successfully!")

def remove_book():
    title = input("Enter the title of the book to remove: ")
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    print("Book removed successfully!")

def search_book():
    choice = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
    query = input("Enter the search term: ").strip().lower()
    
    if choice == "1":
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ?", (f"%{query}%",))
    elif choice == "2":
        cursor.execute("SELECT * FROM books WHERE LOWER(author) LIKE ?", (f"%{query}%",))
    
    results = cursor.fetchall()
    
    if results:
        for idx, book in enumerate(results, 1):
            print(f"{idx}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
    else:
        print("No matching books found.")

def display_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    if not books:
        print("Your library is empty.")
    else:
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")

def display_statistics():
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    print(f"Total books: {total_books}")
    print(f"Percentage read: {percentage_read:.2f}%")

def main():
    while True:
        print("\nMenu\n1. Add a book\n2. Remove a book\n3. Search for a book\n4. Display all books\n5. Display statistics\n6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            conn.close()
            print("Library saved to database. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
