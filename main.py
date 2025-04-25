try:
    input = raw_input
except NameError:
    pass

import csv
import os
import datetime

# File names for data persistence
BOOKS_FILE = "books.csv"
MEMBERS_FILE = "members.csv"
BORROWS_FILE = "borrows.csv"


# ------------------------------
# Data Persistence Functions
# ------------------------------

def load_books():
    books = []
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["times_borrowed"] = int(row.get("times_borrowed", 0))
                row["available"] = True if row.get("available", "True") == "True" else False
                books.append(row)
    return books


def save_books(books):
    fieldnames = ["book_id", "title", "author", "genre", "publication_year", "available", "times_borrowed"]
    with open(BOOKS_FILE, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            book_copy = book.copy()
            book_copy["available"] = "True" if book["available"] else "False"
            writer.writerow(book_copy)


def load_members():
    members = []
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                members.append(row)
    return members


def save_members(members):
    fieldnames = ["member_id", "name", "contact_info"]
    with open(MEMBERS_FILE, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for member in members:
            writer.writerow(member)


def load_borrows():
    borrows = []
    if os.path.exists(BORROWS_FILE):
        with open(BORROWS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                borrows.append(row)
    return borrows


def save_borrows(borrows):
    fieldnames = ["borrow_id", "book_id", "member_id", "borrow_date", "return_date", "late_fee"]
    with open(BORROWS_FILE, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for borrow in borrows:
            writer.writerow(borrow)


def generate_id(prefix):
    return prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


# ------------------------------
# Book Management Functions
# ------------------------------

def add_book(books):
    book_id = input("Enter book ID: ").strip()
    for book in books:
        if book["book_id"] == book_id:
            print("Book ID already exists.")
            return
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    genre = input("Enter genre: ").strip()
    publication_year = input("Enter publication year: ").strip()
    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "genre": genre,
        "publication_year": publication_year,
        "available": True,
        "times_borrowed": 0
    }
    books.append(new_book)
    print("Book added successfully.")


def update_book(books):
    book_id = input("Enter book ID to update: ").strip()
    for book in books:
        if book["book_id"] == book_id:
            print("Leave field empty to keep current value.")
            new_title = input("Enter new title (current: {}): ".format(book["title"])).strip()
            new_author = input("Enter new author (current: {}): ".format(book["author"])).strip()
            new_genre = input("Enter new genre (current: {}): ".format(book["genre"])).strip()
            new_pub_year = input("Enter new publication year (current: {}): ".format(book["publication_year"])).strip()
            if new_title:
                book["title"] = new_title
            if new_author:
                book["author"] = new_author
            if new_genre:
                book["genre"] = new_genre
            if new_pub_year:
                book["publication_year"] = new_pub_year
            print("Book updated successfully.")
            return
    print("Book not found.")


def delete_book(books, borrows):
    book_id = input("Enter book ID to delete: ").strip()
    for i, book in enumerate(books):
        if book["book_id"] == book_id:
            for borrow in borrows:
                if borrow["book_id"] == book_id and borrow["return_date"] == "":
                    print("Cannot delete book; it is currently borrowed.")
                    return
            del books[i]
            print("Book deleted successfully.")
            return
    print("Book not found.")


def search_books(books):
    criterion = input("Search by (title/author/genre): ").strip().lower()
    keyword = input("Enter search keyword: ").strip().lower()
    results = []
    for book in books:
        if criterion == "title" and keyword in book["title"].lower():
            results.append(book)
        elif criterion == "author" and keyword in book["author"].lower():
            results.append(book)
        elif criterion == "genre" and keyword in book["genre"].lower():
            results.append(book)
    if results:
        for book in results:
            status = "Available" if book["available"] else "Borrowed"
            print("ID: {0}, Title: {1}, Author: {2}, Genre: {3}, Year: {4}, Status: {5}".format(
                book["book_id"], book["title"], book["author"], book["genre"], book["publication_year"], status))
    else:
        print("No matching books found.")


# ------------------------------
# Member Management Functions
# ------------------------------

def add_member(members):
    member_id = input("Enter member ID: ").strip()
    for member in members:
        if member["member_id"] == member_id:
            print("Member ID already exists.")
            return
    name = input("Enter member name: ").strip()
    contact_info = input("Enter contact information: ").strip()
    new_member = {
        "member_id": member_id,
        "name": name,
        "contact_info": contact_info
    }
    members.append(new_member)
    print("Member added successfully.")


def update_member(members):
    member_id = input("Enter member ID to update: ").strip()
    for member in members:
        if member["member_id"] == member_id:
            print("Leave field empty to keep current value.")
            new_name = input("Enter new name (current: {}): ".format(member["name"])).strip()
            new_contact = input("Enter new contact info (current: {}): ".format(member["contact_info"])).strip()
            if new_name:
                member["name"] = new_name
            if new_contact:
                member["contact_info"] = new_contact
            print("Member updated successfully.")
            return
    print("Member not found.")


def view_members(members):
    if members:
        for member in members:
            print("ID: {0}, Name: {1}, Contact: {2}".format(member["member_id"], member["name"], member["contact_info"]))
    else:
        print("No members registered.")


def delete_member(members, borrows):
    member_id = input("Enter member ID to delete: ").strip()
    for borrow in borrows:
        if borrow["member_id"] == member_id and borrow["return_date"] == "":
            print("Cannot delete member; they currently have borrowed books.")
            return
    for i, member in enumerate(members):
        if member["member_id"] == member_id:
            del members[i]
            print("Member deleted successfully.")
            return
    print("Member not found.")


# ------------------------------
# Borrow and Return Functions
# ------------------------------

# For Admin operations (member ID is provided manually)
def borrow_book(books, members, borrows):
    member_id = input("Enter member ID: ").strip()
    if not any(member["member_id"] == member_id for member in members):
        print("Member not found.")
        return
    book_id = input("Enter book ID to borrow: ").strip()
    for book in books:
        if book["book_id"] == book_id:
            if not book["available"]:
                print("Book is currently not available.")
                return
            borrow_date = input("Enter borrow date (YYYY-MM-DD) or leave blank for today: ").strip()
            if not borrow_date:
                borrow_date = datetime.date.today().strftime("%Y-%m-%d")
            borrow_id = generate_id("BR")
            new_borrow = {
                "borrow_id": borrow_id,
                "book_id": book_id,
                "member_id": member_id,
                "borrow_date": borrow_date,
                "return_date": "",
                "late_fee": "0"
            }
            borrows.append(new_borrow)
            book["available"] = False
            book["times_borrowed"] += 1
            print("Book borrowed successfully.")
            return
    print("Book not found.")


def return_book(books, borrows):
    book_id = input("Enter book ID to return: ").strip()
    for borrow in borrows:
        if borrow["book_id"] == book_id and borrow["return_date"] == "":
            return_date = input("Enter return date (YYYY-MM-DD) or leave blank for today: ").strip()
            if not return_date:
                return_date = datetime.date.today().strftime("%Y-%m-%d")
            borrow_date_obj = datetime.datetime.strptime(borrow["borrow_date"], "%Y-%m-%d").date()
            return_date_obj = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
            days_borrowed = (return_date_obj - borrow_date_obj).days
            late_fee = 0
            if days_borrowed > 14:
                late_fee = days_borrowed - 14
            borrow["return_date"] = return_date
            borrow["late_fee"] = str(late_fee)
            for book in books:
                if book["book_id"] == book_id:
                    book["available"] = True
                    break
            print("Book returned successfully. Late fee: ${}".format(late_fee))
            return
    print("Borrow record not found or book already returned.")


def view_borrowed_books(books, members, borrows):
    active_borrows = [b for b in borrows if b["return_date"] == ""]
    if active_borrows:
        for borrow in active_borrows:
            book_title = next((book["title"] for book in books if book["book_id"] == borrow["book_id"]), "Unknown")
            member_name = next((member["name"] for member in members if member["member_id"] == borrow["member_id"]), "Unknown")
            print("Borrow ID: {0}, Book: {1} (ID: {2}), Member: {3} (ID: {4}), Borrow Date: {5}".format(
                borrow["borrow_id"], book_title, borrow["book_id"], member_name, borrow["member_id"], borrow["borrow_date"]))
    else:
        print("No active borrow records.")


# For Member operations (logged-in member; their ID is used automatically)
def member_borrow_book(member, books, borrows):
    book_id = input("Enter book ID to borrow: ").strip()
    for book in books:
        if book["book_id"] == book_id:
            if not book["available"]:
                print("Book is currently not available.")
                return
            borrow_date = input("Enter borrow date (YYYY-MM-DD) or leave blank for today: ").strip()
            if not borrow_date:
                borrow_date = datetime.date.today().strftime("%Y-%m-%d")
            borrow_id = generate_id("BR")
            new_borrow = {
                "borrow_id": borrow_id,
                "book_id": book_id,
                "member_id": member["member_id"],
                "borrow_date": borrow_date,
                "return_date": "",
                "late_fee": "0"
            }
            borrows.append(new_borrow)
            book["available"] = False
            book["times_borrowed"] += 1
            print("Book borrowed successfully.")
            return
    print("Book not found.")


def member_return_book(member, books, borrows):
    book_id = input("Enter book ID to return: ").strip()
    for borrow in borrows:
        if (borrow["book_id"] == book_id and
            borrow["member_id"] == member["member_id"] and
            borrow["return_date"] == ""):
            return_date = input("Enter return date (YYYY-MM-DD) or leave blank for today: ").strip()
            if not return_date:
                return_date = datetime.date.today().strftime("%Y-%m-%d")
            borrow_date_obj = datetime.datetime.strptime(borrow["borrow_date"], "%Y-%m-%d").date()
            return_date_obj = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
            days_borrowed = (return_date_obj - borrow_date_obj).days
            late_fee = 0
            if days_borrowed > 14:
                late_fee = days_borrowed - 14
            borrow["return_date"] = return_date
            borrow["late_fee"] = str(late_fee)
            for book in books:
                if book["book_id"] == book_id:
                    book["available"] = True
                    break
            print("Book returned successfully. Late fee: ${}".format(late_fee))
            return
    print("Borrow record not found or this book was not borrowed by you.")


def view_member_borrowed_books(member, books, borrows):
    member_borrows = [b for b in borrows if b["member_id"] == member["member_id"] and b["return_date"] == ""]
    if member_borrows:
        for borrow in member_borrows:
            book_title = next((book["title"] for book in books if book["book_id"] == borrow["book_id"]), "Unknown")
            print("Borrow ID: {0}, Book: {1} (ID: {2}), Borrow Date: {3}".format(
                borrow["borrow_id"], book_title, borrow["book_id"], borrow["borrow_date"]))
    else:
        print("You have no active borrowed books.")


# ------------------------------
# Search and Reporting Functions
# ------------------------------

def search_available_books(books):
    available_books = [book for book in books if book["available"]]
    if available_books:
        for book in available_books:
            print("ID: {0}, Title: {1}, Author: {2}, Genre: {3}, Year: {4}".format(
                book["book_id"], book["title"], book["author"], book["genre"], book["publication_year"]))
    else:
        print("No available books.")


def list_overdue_books(books, members, borrows):
    today = datetime.date.today()
    overdue_found = False
    for borrow in borrows:
        if borrow["return_date"] == "":
            borrow_date = datetime.datetime.strptime(borrow["borrow_date"], "%Y-%m-%d").date()
            days_borrowed = (today - borrow_date).days
            if days_borrowed > 14:
                late_fee = days_borrowed - 14
                member_name = next((member["name"] for member in members if member["member_id"] == borrow["member_id"]), "Unknown")
                book_title = next((book["title"] for book in books if book["book_id"] == borrow["book_id"]), "Unknown")
                print("Borrow ID: {0}, Book: {1} (ID: {2}), Member: {3} (ID: {4}), Borrow Date: {5}, Overdue by {6} days, Late Fee: ${7}".format(
                    borrow["borrow_id"], book_title, borrow["book_id"], member_name, borrow["member_id"],
                    borrow["borrow_date"], days_borrowed - 14, late_fee))
                overdue_found = True
    if not overdue_found:
        print("No overdue books.")


def generate_reports(books, borrows):
    total_books = len(books)
    borrowed_books_count = sum(1 for b in borrows if b["return_date"] == "")
    popular_books = sorted(books, key=lambda b: b["times_borrowed"], reverse=True)
    print("=== Reports ===")
    print("Total number of books: {}".format(total_books))
    print("Number of borrowed books: {}".format(borrowed_books_count))
    print("Popular Books (most borrowed):")
    for book in popular_books:
        print("Title: {}, Times Borrowed: {}".format(book["title"], book["times_borrowed"]))


# ------------------------------
# Menus and Login Functions
# ------------------------------

def admin_menu():
    # Load data for admin session
    books = load_books()
    members = load_members()
    borrows = load_borrows()
    while True:
        print("\n==== Admin Menu ====")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow/Return")
        print("4. Search/Reporting")
        print("5. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            while True:
                print("\n--- Book Management ---")
                print("1. Add Book")
                print("2. Update Book")
                print("3. Delete Book")
                print("4. Search Books")
                print("5. Back to Admin Menu")
                sub_choice = input("Enter your choice: ").strip()
                if sub_choice == "1":
                    add_book(books)
                elif sub_choice == "2":
                    update_book(books)
                elif sub_choice == "3":
                    delete_book(books, borrows)
                elif sub_choice == "4":
                    search_books(books)
                elif sub_choice == "5":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "2":
            while True:
                print("\n--- Member Management ---")
                print("1. Register New Member")
                print("2. Update Member")
                print("3. View All Members")
                print("4. Delete Member")
                print("5. Back to Admin Menu")
                sub_choice = input("Enter your choice: ").strip()
                if sub_choice == "1":
                    add_member(members)
                elif sub_choice == "2":
                    update_member(members)
                elif sub_choice == "3":
                    view_members(members)
                elif sub_choice == "4":
                    delete_member(members, borrows)
                elif sub_choice == "5":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "3":
            while True:
                print("\n--- Borrow/Return ---")
                print("1. Borrow Book")
                print("2. Return Book")
                print("3. View Borrowed Books")
                print("4. Back to Admin Menu")
                sub_choice = input("Enter your choice: ").strip()
                if sub_choice == "1":
                    borrow_book(books, members, borrows)
                elif sub_choice == "2":
                    return_book(books, borrows)
                elif sub_choice == "3":
                    view_borrowed_books(books, members, borrows)
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "4":
            while True:
                print("\n--- Search/Reporting ---")
                print("1. Search Available Books")
                print("2. List Overdue Books")
                print("3. Generate Reports")
                print("4. Back to Admin Menu")
                sub_choice = input("Enter your choice: ").strip()
                if sub_choice == "1":
                    search_available_books(books)
                elif sub_choice == "2":
                    list_overdue_books(books, members, borrows)
                elif sub_choice == "3":
                    generate_reports(books, borrows)
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "5":
            # Save data and logout
            save_books(books)
            save_members(members)
            save_borrows(borrows)
            print("Data saved. Logging out of Admin session...")
            break
        else:
            print("Invalid choice. Please try again.")


def member_menu(member):
    books = load_books()
    borrows = load_borrows()
    while True:
        print("\n==== Member Menu ====")
        print("Welcome, {0}".format(member["name"]))
        print("1. View Available Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. View My Borrowed Books")
        print("5. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            search_available_books(books)
        elif choice == "2":
            member_borrow_book(member, books, borrows)
        elif choice == "3":
            member_return_book(member, books, borrows)
        elif choice == "4":
            view_member_borrowed_books(member, books, borrows)
        elif choice == "5":
            save_books(books)
            save_borrows(borrows)
            print("Data saved. Logging out of Member session...")
            break
        else:
            print("Invalid choice. Please try again.")


def admin_login():
    print("\n=== Admin Login ===")
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    if username == "admin" and password == "admin123":
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin credentials.")


def member_login():
    print("\n=== Member Login ===")
    member_id = input("Enter your member ID: ").strip()
    members = load_members()
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    if member:
        print("Member login successful. Welcome, {0}!".format(member["name"]))
        member_menu(member)
    else:
        print("Member not found.")


def login_menu():
    while True:
        print("\n==== Welcome to the Library Management System ====")
        print("1. Admin Login")
        print("2. Member Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            admin_login()
        elif choice == "2":
            member_login()
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    login_menu()