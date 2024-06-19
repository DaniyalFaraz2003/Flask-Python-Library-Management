# models.py


class Book:
    def __init__(self, bookid, author, title, isbn, category, year, language):
        self.bookid = bookid
        self.author = author
        self.title = title
        self.isbn = isbn
        self.category = category
        self.year = year
        self.language = language

    def __lt__(self, other):
        return self.bookid < other.bookid

    def __eq__(self, other):
        return self.bookid == other.bookid

class Periodical(Book):
    def __init__(self, bookid, author, title, isbn, category, year, language):
        super().__init__(bookid, author, title, isbn, category, year, language)

class AudioBook(Book):
    def __init__(self, bookid, author, title, isbn, category, year, language, audio_format):
        super().__init__(bookid, author, title, isbn, category, year, language)
        self.audio_format = audio_format

class BorrowedItem:
    def __init__(self, borrowerid, bookid, borrowdate):
        self.borrowerid = borrowerid
        self.bookid = bookid
        self.borrowdate = borrowdate

class Borrower:
    def __init__(self, borrowerid, firstname, lastname, email, password, role):
        self.borrowerid = borrowerid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role

class LibraryAdministrator:
    def __init__(self, adminid, firstname, lastname, email, password):
        self.adminid = adminid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
