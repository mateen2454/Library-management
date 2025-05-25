books_list = []  # Main book catalog
borrower_records = {}  # Borrower database
all_transactions = []  # Transaction history

class Book:
    def __init__(self, bid, title, author, qty=1):
        self.id = bid
        self.title = title
        self.author = author
        self.total_copies = qty
        self.available_copies = qty

    def __repr__(self):
        status = "Available" if self.available_copies > 0 else "Checked out"
        return f"Book #{self.id}: '{self.title}' by {self.author} ({status})"

class Borrower:
    def __init__(self, borrower_id, full_name):
        self.borrower_id = borrower_id
        self.name = full_name
        self.current_loans = []  # Books currently borrowed

class TransactionLog:
    def __init__(self, book_id, borrower_id, action_type):
        self.book_id = book_id
        self.borrower_id = borrower_id
        self.action = action_type
        self.date = "2023-12-03" 

# Helper function to get valid user input
def get_user_input(prompt, input_type=str, min_val=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Oops, please enter something!")
            continue

        try:
            if input_type == int:
                value = int(user_input)
                if min_val is not None and value < min_val:
                    print(f"Please enter a number at least {min_val}.")
                    continue
                return value
            return user_input  # Default to string
        except ValueError:
            print("Whoops! Please enter a valid number.")

# Find a book by ID
def locate_book(book_id):
    for book in books_list:
        if book.id == book_id:
            return book
    return None

# Find a borrower by ID
def find_borrower(borrower_id):
    return borrower_records.get(borrower_id)

# Add a new book to the catalog
def add_new_book():
    print("\n📚 Adding a New Book 📚")
    book_id = get_user_input("Enter a unique book ID: ", int, 1)

    if locate_book(book_id):
        print("Uh-oh! That book ID is already taken. Try a different one.")
        return

    title = get_user_input("What's the book title? ")
    author = get_user_input("Who's the author? ")
    copies = get_user_input("How many copies? (Default is 1): ", int, 1) or 1

    books_list.append(Book(book_id, title, author, copies))
    print(f"Success! Added {copies} copy/copies of '{title}' by {author} to the library.")

# Register a new borrower
def register_new_borrower():
    print("\n👤 Registering a New Borrower 👤")
    borrower_id = get_user_input("Enter a unique borrower ID: ", int, 1)

    if borrower_id in borrower_records:
        print("Oops! That borrower ID is already in use. Choose another.")
        return

    name = get_user_input("What's the borrower's full name? ")
    borrower_records[borrower_id] = Borrower(borrower_id, name)
    print(f"Welcome aboard, {name}! You're now registered with ID {borrower_id}.")

# Check out a book
def checkout_book():
    print("\n📖 Checking Out a Book 📖")
    book_id = get_user_input("Enter the book ID: ", int, 1)
    borrower_id = get_user_input("Enter the borrower ID: ", int, 1)

    book = locate_book(book_id)
    borrower = find_borrower(borrower_id)

    if not book:
        print("Sorry, we couldn't find that book in our catalog.")
        return

    if not borrower:
        print("Hmm, that borrower ID isn't registered. Please register first.")
        return

    if book.available_copies < 1:
        print(f"Oh no! All copies of '{book.title}' are currently checked out.")
        return

    if len(borrower.current_loans) >= 5:  # Max 5 books per borrower
        print(f"Sorry, {borrower.name} has reached the borrowing limit (5 books).")
        return

    book.available_copies -= 1
    borrower.current_loans.append(book_id)
    all_transactions.append(TransactionLog(book_id, borrower_id, "Borrow"))
    print(f"Success! '{book.title}' has been checked out to {borrower.name}.")

# Return a book
def return_book():
    print("\n🔙 Returning a Book 🔙")
    book_id = get_user_input("Enter the book ID: ", int, 1)
    borrower_id = get_user_input("Enter the borrower ID: ", int, 1)

    book = locate_book(book_id)
    borrower = find_borrower(borrower_id)

    if not book:
        print("Sorry, that book isn't in our catalog.")
        return

    if not borrower:
        print("Hmm, that borrower ID isn't registered.")
        return

    if book_id not in borrower.current_loans:
        print(f"{borrower.name} doesn't have '{book.title}' checked out.")
        return

    book.available_copies += 1
    borrower.current_loans.remove(book_id)
    all_transactions.append(TransactionLog(book_id, borrower_id, "Return"))
    print(f"Thank you! '{book.title}' has been returned by {borrower.name}.")

# Search for books by title or author
def search_books():
    print("\n🔍 Searching the Library 🔍")
    query = get_user_input("Enter a title or author to search for: ").lower()
    found = False

    for book in books_list:
        if query in book.title.lower() or query in book.author.lower():
            print(book)
            found = True

    if not found:
        print("No books found matching your search. Try again!")

# View transaction history
def view_transactions():
    print("\n📜 Transaction History 📜")
    if not all_transactions:
        print("No transactions yet!")
        return

    for transaction in all_transactions:
        book = locate_book(transaction.book_id)
        borrower = find_borrower(transaction.borrower_id)
        book_title = book.title if book else f"Book #{transaction.book_id}"
        borrower_name = borrower.name if borrower else f"Borrower #{transaction.borrower_id}"
        print(f"{transaction.date}: {borrower_name} {transaction.action}ed '{book_title}'")

# Main menu
def main_menu():
    while True:
        print("\n=== Welcome to the Library System! ===")
        print("1. Add a new book")
        print("2. Register a new borrower")
        print("3. Check out a book")
        print("4. Return a book")
        print("5. Search for books")
        print("6. View transaction history")
        print("0. Exit")
        
        choice = get_user_input("What would you like to do? ", int)

        if choice == 1:
            add_new_book()
        elif choice == 2:
            register_new_borrower()
        elif choice == 3:
            checkout_book()
        elif choice == 4:
            return_book()
        elif choice == 5:
            search_books()
        elif choice == 6:
            view_transactions()
        elif choice == 0:
            print("Thanks for using the Library System! Goodbye!")
            break
        else:
            print("That's not a valid option. Please choose again.")

if __name__ == '__main__':
    print("Starting the Library System... 📚")
    main_menu()