import os
import io

script_dir = os.path.dirname(os.path.abspath(__file__))

books_file_path = os.path.join(script_dir, "books.csv")
members_file_path = os.path.join(script_dir, "members.csv")
borrows_file_path = os.path.join(script_dir, "borrows.csv")

csv_data = {
    books_file_path: u"""book_id,title,author,genre,publication_year,available,times_borrowed
B001,1984,George Orwell,Dystopian,1949,True,5
B002,To Kill a Mockingbird,Harper Lee,Classic,1960,False,3
B003,The Great Gatsby,F. Scott Fitzgerald,Classic,1925,True,2
""",
    members_file_path: u"""member_id,name,contact_info
M001,John Doe,johndoe@example.com
M002,Jane Smith,janesmith@example.com
M003,Bob Johnson,bobjohnson@example.com
""",
    borrows_file_path: u"""borrow_id,book_id,member_id,borrow_date,return_date,late_fee
BR20250219101010000000,B002,M001,2025-02-01,2025-02-15,0
BR20250219101020000000,B001,M002,2025-02-10,,0
"""
}

for file_path, content in csv_data.items():
    # Use io.open with encoding="utf-8"
    with io.open(file_path, mode="w", encoding="utf-8") as f:
        f.write(content)
    print("{} created in {}.".format(os.path.basename(file_path), script_dir))