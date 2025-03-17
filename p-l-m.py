import json

# File to store book data
LIBRARY_FILE = "library.json"

# Load existing library data
try:
    with open(LIBRARY_FILE, "r") as file:
        library = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    library = []

def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    
    library.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    })
    print("Book added successfully!")
    save_library()

def remove_book():
    title = input("Enter the title of the book to remove: ")
    global library
    library = [book for book in library if book["title"].lower() != title.lower()]
    print("Book removed successfully!")
    save_library()

def search_book():
    choice = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
    query = input("Enter the search term: ").strip().lower()
    
    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]
    
    if results:
        for idx, book in enumerate(results, 1):
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("No matching books found.")

def display_books():
    if not library:
        print("Your library is empty.")
    else:
        for idx, book in enumerate(library, 1):
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
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
            save_library()
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
