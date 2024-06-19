# data_structures.py

from models import Book, BorrowedItem

class TreeNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class LibraryTree:
    def __init__(self):
        self.root = None

    def insert(self, book):
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be inserted into the LibraryTree")
        if self.root is None:
            self.root = TreeNode(book)
        else:
            self._insert(self.root, book)

    def _insert(self, node, book):
        if book < node.book:
            if node.left is None:
                node.left = TreeNode(book)
            else:
                self._insert(node.left, book)
        else:
            if node.right is None:
                node.right = TreeNode(book)
            else:
                self._insert(node.right, book)

    def search(self, bookid):
        return self._search(self.root, bookid)

    def _search(self, node, bookid):
        if node is None or node.book.bookid == bookid:
            return node.book if node else None
        if bookid < node.book.bookid:
            return self._search(node.left, bookid)
        return self._search(node.right, bookid)
    
    def search_all(self, bookids):
        results = []
        for bookid in bookids:
            book = self.search(bookid)
            if book:
                results.append(book)
        return results

    def clear(self):
        self.root = None

class DoublyLinkedListNode:
    def __init__(self, borrower):
        self.borrower = borrower
        self.next = None
        self.prev = None

class BorrowerList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, borrower):
        new_node = DoublyLinkedListNode(borrower)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def find(self, borrowerid):
        current = self.head
        while current:
            if current.borrower.borrowerid == borrowerid:
                return current.borrower
            current = current.next
        return None

    def remove(self, borrowerid):
        current = self.head
        while current:
            if current.borrower.borrowerid == borrowerid:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return current.borrower
            current = current.next
        return None

    def update(self, borrowerid, firstname=None, lastname=None, email=None, password=None, role=None):
        borrower = self.find(borrowerid)
        if borrower:
            if firstname:
                borrower.firstname = firstname
            if lastname:
                borrower.lastname = lastname
            if email:
                borrower.email = email
            if password:
                borrower.password = password
            if role:
                borrower.role = role
            return borrower
        return None

    def clear(self):
        self.head = None
        self.tail = None


class BorrowedItems:
    def __init__(self):
        self.items = []

    def add_item(self, borrowerid, bookid, borrowdate):
        self.items.append(BorrowedItem(borrowerid, bookid, borrowdate))

    def get_borrowed_items(self, borrowerid):
        return [item for item in self.items if item.borrowerid == borrowerid]

    def return_item(self, borrowerid, bookid):
        for item in self.items:
            if item.borrowerid == borrowerid and item.bookid == bookid:
                self.items.remove(item)
                return item
        return None
    
    def clear(self):
        self.items = []
