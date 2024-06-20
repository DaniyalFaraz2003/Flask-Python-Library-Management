# test_library.py

from datetime import datetime, timedelta
from models import Book, Periodical, AudioBook, Borrower
from data_structures import LibraryTree, BorrowerList, BorrowedItems

def main():
    # Initialize the LibraryTree
    library_tree = LibraryTree()
    

    # Create Book, Periodical, Magazine, and AudioBook instances
    book1 = Book(1, "Author A", "Book A", "ISBN0001", "Fiction", datetime(2020, 1, 1), "English")
    book2 = Periodical(2, "Author B", "Periodical B", "ISBN0002", "Science", datetime(2021, 2, 2), "English")
    book3 = AudioBook(3, "Author C", "Magazine C", "ISBN0003", "Lifestyle", datetime(2022, 3, 3), "English", "MP3")
    book4 = AudioBook(4, "Author D", "AudioBook D", "ISBN0004", "Adventure", datetime(2023, 4, 4), "English", "MP3")

    # Insert books into the LibraryTree
    library_tree.insert(book1)
    library_tree.insert(book2)
    library_tree.insert(book3)
    library_tree.insert(book4)

    # Search for books in the LibraryTree
    print("Search for Book ID 1:", library_tree.search(1))  # Should find book1
    print("Search for Book ID 2:", library_tree.search(2))  # Should find book2
    print("Search for Book ID 3:", library_tree.search(3))  # Should find book3
    print("Search for Book ID 4:", library_tree.search(4))  # Should find book4
    print("Search for Book ID 5:", library_tree.search(5))  # Should return None
    print("Search for Book ID [1, 2, 3]:", library_tree.search_all([1, 2, 3]))  # Should return None

    # Initialize the BorrowerList
    borrower_list = BorrowerList()

    # Create Borrower instances
    borrower1 = Borrower(1, "John", "Doe", "john.doe@example.com", "password123", "User")
    borrower2 = Borrower(2, "Jane", "Smith", "jane.smith@example.com", "password456", "User")

    # Append borrowers to the BorrowerList
    borrower_list.append(borrower1)
    borrower_list.append(borrower2)

    # Find and display a borrower
    print("Find Borrower ID 1:", borrower_list.find(1))  # Should find borrower1
    print("Find Borrower ID 2:", borrower_list.find(2))  # Should find borrower2
    print("Find Borrower ID 3:", borrower_list.find(3))  # Should return None

    # Initialize the BorrowedItems
    borrowed_items = BorrowedItems()

    # Add borrowed items
    current_date = datetime.now()
    borrowed_items.add_item(1, 1, current_date)
    borrowed_items.add_item(1, 2, current_date)
    borrowed_items.add_item(2, 3, current_date)

    # Get borrowed items for a borrower
    print("Borrowed items for Borrower ID 1:", borrowed_items.get_borrowed_items(1))  # Should list items borrowed by borrower1
    print("Borrowed items for Borrower ID 2:", borrowed_items.get_borrowed_items(2))  # Should list items borrowed by borrower2

    # Return an item
    print("Return item for Borrower ID 1, Book ID 1:", borrowed_items.return_item(1, 1))  # Should return the borrowed item
    print("Borrowed items for Borrower ID 1 after return:", borrowed_items.get_borrowed_items(1))  # Should update the list

if __name__ == "__main__":
    main()
