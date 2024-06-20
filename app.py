from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb
import MySQLdb.cursors
import re
import os
import random
import sys
from datetime import datetime, timedelta

# Import the classes
from models import Book, Periodical, AudioBook, Borrower, BorrowedItem
from data_structures import LibraryTree, BorrowerList, BorrowedItems

app = Flask(__name__)

app.secret_key = 'abcd2123445'  
db=MySQLdb.connect(host="localhost",user="root",
                password="",database="library_management")
cursor = db.cursor(MySQLdb.cursors.DictCursor)



# populate the data structures
# Global instances of data structures
library_tree = LibraryTree()
borrower_list = BorrowerList()
borrowed_items = BorrowedItems()

# Function to populate data structures from the database
def populate_data_structures():
    populate_library_tree()
    populate_borrower_list()
    populate_borrowed_items()

def populate_library_tree():
    library_tree.clear()
    
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()

    # Fetch all audiobooks
    cursor.execute("SELECT * FROM audiobook")
    audiobooks = cursor.fetchall()
    audiobook_dict = {ab['bookid']: ab['audioformat'] for ab in audiobooks}

    cursor.execute("SELECT * FROM periodical")
    periodicals = cursor.fetchall()
    periodical_list = [p['bookid'] for p in periodicals]

    for book_data in books:
        if book_data['bookid'] in periodical_list:
            book = Periodical(
                book_data['bookid'], book_data['author'], book_data['title'],
                book_data['isbn'], book_data['category'], book_data['year'],
                book_data['language']
            )
        elif book_data['bookid'] in audiobook_dict.keys():
            audioformat = audiobook_dict[book_data['bookid']]
            book = AudioBook(
                book_data['bookid'], book_data['author'], book_data['title'],
                book_data['isbn'], book_data['category'], book_data['year'],
                book_data['language'], audioformat
            )
        else:
            book = Book(
                book_data['bookid'], book_data['author'], book_data['title'],
                book_data['isbn'], book_data['category'], book_data['year'],
                book_data['language']
            )
        library_tree.insert(book)



def populate_borrower_list():
    borrower_list.clear()
    cursor.execute("SELECT * FROM borrower")
    borrowers = cursor.fetchall()
    for borrower_data in borrowers:
        borrower = Borrower(
            borrower_data['borrowerid'], borrower_data['firstname'],
            borrower_data['lastname'], borrower_data['email'],
            borrower_data['password'], borrower_data['role']
        )
        borrower_list.append(borrower)

def populate_borrowed_items():
    borrowed_items.clear()
    cursor.execute("SELECT * FROM borrowed")
    borrowed_records = cursor.fetchall()
    for record in borrowed_records:
        borrowed_items.add_item(
            record['borrowerid'], record['bookid'], record['borrowdate']
        )


# Call the populate function on startup
populate_data_structures()


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        user = borrower_list.findWithEmailPassword(email, password)
        if user:
            session['loggedin'] = True
            session['userid'] = user.borrowerid
            session['name'] = user.firstname
            session['email'] = user.email
            session['role'] = user.role
            mesage = 'Logged in successfully !'            
            if user.role == "admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('borrower'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
    
# Route for borrowing a book
@app.route("/borrow_book")
def borrow_book():
    if 'loggedin' in session:
        borrowBookId = request.args.get('bookid')
        error_message = ""
        
        # Count current borrowed unreturned books
        cursor.execute("""
            SELECT COUNT(*) AS num_borrowed
            FROM borrowed
            WHERE borrowerid = %s AND returndate = '0000-00-00 00:00:00'
        """, (session['userid'],))
        num_borrowed_unreturned = cursor.fetchone()['num_borrowed']
        
        # Check if there are any unpaid fines
        cursor.execute("""
            SELECT COUNT(*) AS num_unpaid_fines
            FROM fine f
            JOIN borrowed b ON f.borrowedid = b.borrowedid
            WHERE b.borrowerid = %s AND f.status = 'unpaid'
        """, (session['userid'],))
        num_unpaid_fines = cursor.fetchone()['num_unpaid_fines']
        
        # Only allow borrowing if conditions are met
        if num_borrowed_unreturned < 8 and num_unpaid_fines == 0:
            current_date = datetime.now().date()
            three_months_later = current_date + timedelta(days=90)  # Approximation of 3 months

            cursor.execute("""
                INSERT INTO borrowed (bookid, borrowerid, borrowdate, duedate, returndate)
                VALUES (%s, %s, %s, %s, 'NULL')
            """, (borrowBookId, session['userid'], current_date, three_months_later))
            db.commit()

            borrowed_items.add_item(session['userid'], borrowBookId, current_date)
            
        else:
            # Handle case where conditions are not met
            if num_borrowed_unreturned >= 8:
                error_message = "You have reached the maximum limit of borrowed unreturned books."
            elif num_unpaid_fines > 0:
                error_message = "You have unpaid fines. Please clear your fines before borrowing."
            
        return redirect(url_for("borrower"))
        
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'email' in request.form :
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']
        role = "borrower"
        
        cursor.execute('SELECT * FROM borrower WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not firstname or not lastname or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO borrower (firstname, lastname, email, password, role) VALUES (% s, % s, % s, %s, %s)', (firstname, lastname, email, password, role))
            db.commit()
            mesage = 'You have successfully registered !'
            borrower_list.append(Borrower(cursor.lastrowid, firstname, lastname, email, password, role))
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route('/view_book', methods=['GET'])
def view_book():
    # SQL query to get book details and its type (book, periodical, audiobook)
    viewBookId = request.args.get('bookid')
    # sql_query = """
    # SELECT b.bookid, b.title, b.author, b.isbn, b.category, b.year, b.language,
    #         CASE
    #             WHEN p.bookid IS NOT NULL THEN 'Periodical'
    #             WHEN a.bookid IS NOT NULL THEN 'Audiobook'
    #             ELSE 'Book'
    #         END AS book_type,
    #         a.audioformat
    # FROM book b
    # LEFT JOIN periodical p ON b.bookid = p.bookid
    # LEFT JOIN audiobook a ON b.bookid = a.bookid
    # WHERE b.bookid = %s
    # """

    # cursor.execute(sql_query, (viewBookId,))
    # book = cursor.fetchone()
    book = dict().fromkeys(['bookid', 'title', 'author', 'isbn', 'category', 'year', 'language', 'book_type', 'audioformat'], None)
    retrieved_book = library_tree.search(int(viewBookId))
    if retrieved_book:
        book['bookid'] = retrieved_book.bookid
        book['title'] = retrieved_book.title
        book['author'] = retrieved_book.author
        book['isbn'] = retrieved_book.isbn
        book['category'] = retrieved_book.category
        book['year'] = retrieved_book.year
        book['language'] = retrieved_book.language
        if type(retrieved_book) is AudioBook: 
            book['book_type'] = "Audiobook"
            book['audioformat'] = retrieved_book.audio_format
        elif type(retrieved_book) is Periodical: book['book_type'] = "Periodical"
        else: book['book_type'] = "Book"

    return render_template('viewbook.html', book=book)

@app.route("/borrower", methods =['GET', 'POST']) # 8 books check has to be made
def borrower():
    if 'loggedin' in session:
        
        cursor.execute("""SELECT b.bookid, b.title, b.author, b.isbn, b.category, b.year, b.language FROM book b LEFT JOIN borrowed br ON b.bookid = br.bookid AND br.borrowerid = %s WHERE br.bookid IS NULL OR br.returndate != '0000-00-00 00:00:00';
        """, (session['userid'], ))
        books = cursor.fetchall()    


        return render_template("borrower.html", books = books)
    return redirect(url_for('login'))

@app.route('/return_book', methods=['GET'])
def return_book():
    # SQL query to get book details and its type (book, periodical, audiobook)
    returnId = request.args.get('borrowedid')
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_query = """
    UPDATE borrowed
    SET returndate = %s
    WHERE borrowedid = %s
    """
    cursor.execute(update_query, (current_date, returnId))
    db.commit()
    cursor.execute("SELECT borrowerid, bookid FROM borrowed WHERE borrowedid = %s", (returnId, ))
    record = cursor.fetchone()
    borrowed_items.return_item(record['borrowerid'], record['bookid'])
    return redirect(url_for("borrowed"))

@app.route('/borrowed', methods=['GET'])
def borrowed():
    # SQL query to get borrowed books with status
    sql_query = """
        SELECT br.borrowedid, b.bookid, b.title, b.author, br.borrowdate, br.duedate, br.returndate,
        CASE
            WHEN br.returndate = '0000-00-00 00:00:00' AND br.duedate < %s THEN 'Overdue'
            WHEN br.returndate = '0000-00-00 00:00:00' THEN 'Borrowed'
            ELSE 'Returned'
        END AS status
    FROM borrowed br
    JOIN book b ON br.bookid = b.bookid
    WHERE br.borrowerid = %s
    """

    current_date = datetime.now().date()
    cursor.execute(sql_query, (current_date, session['userid']))
    borrowed_books = cursor.fetchall()

    return render_template('borrowedbooks.html', borrowed_books=borrowed_books)

@app.route('/fines', methods=['GET'])
def fines():
    # SQL query to get fines details
    sql_query = """
    SELECT f.fineid, b.title, br.borrowdate, br.duedate, f.amount, f.status
    FROM fine f
    JOIN borrowed br ON f.borrowedid = br.borrowedid
    JOIN book b ON br.bookid = b.bookid
    WHERE br.borrowerid = %s
    """
    cursor.execute(sql_query, (session['userid'],))
    fines_data = cursor.fetchall()

    return render_template('fines.html', fines=fines_data)

@app.route('/pay_fine', methods=['GET'])
def pay_fine():
    # Update the fine status to 'Paid'
    fineid = request.args.get('fineid')
    update_query = """
    UPDATE fine
    SET status = 'paid'
    WHERE fineid = %s
    """
    cursor.execute(update_query, (fineid,))
    db.commit()

    return redirect(url_for('fines'))

@app.route('/search_book_borrower', methods=['GET'])
def search_book_borrower():
    if 'loggedin' in session:
        search_field = request.args.get('search_field')
        search_value = request.args.get('search_value')

        borrowerid = session['userid']
        
        # Default query to fetch all books that the borrower has not borrowed
        # query = """
        # SELECT b.bookid, b.title, b.author, b.isbn, b.category, b.year, b.language
        # FROM book b
        # LEFT JOIN borrowed br ON b.bookid = br.bookid AND br.borrowerid = %s
        # WHERE (br.bookid IS NULL OR br.returndate != '0000-00-00 00:00:00')
        # """
        query = """
        SELECT b.bookid
        FROM book b
        LEFT JOIN borrowed br ON b.bookid = br.bookid AND br.borrowerid = %s
        WHERE (br.bookid IS NULL OR br.returndate != '0000-00-00 00:00:00')
        """
        params = [borrowerid]

        # If search parameters are provided, modify the query
        if search_field and search_value:
            query += " AND b.{} LIKE %s".format(search_field)
            params.append('%' + search_value + '%')
        
        cursor.execute(query, params)
        books = cursor.fetchall()

        books_list = [dict().fromkeys([
            'bookid', 'title', 'author', 'isbn', 'category', 'year', 'language'
        ], None) for _ in range(len(books))]

        for i in range(len(books)):
            retrieved_book = library_tree.search(int(books[i]['bookid']))
            books_list[i]['bookid'] = retrieved_book.bookid
            books_list[i]['title'] = retrieved_book.title
            books_list[i]['author'] = retrieved_book.author
            books_list[i]['isbn'] = retrieved_book.isbn
            books_list[i]['category'] = retrieved_book.category
            books_list[i]['year'] = retrieved_book.year
            books_list[i]['language'] = retrieved_book.language
        
        return render_template("borrower.html", books=books_list)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
def admin():
    if 'loggedin' in session:
        
        cursor.execute("""SELECT * FROM book;""")
        books = cursor.fetchall()    

        return render_template("admin.html", books = books)
    return redirect(url_for('login'))


@app.route('/adminsearch', methods=['GET', 'POST'])
def adminsearch():
    if 'loggedin' in session and session['role'] == 'admin':
        search_field = request.args.get('search_field')
        search_value = request.args.get('search_value')

        # Default query to fetch all books
        query = "SELECT * FROM book"
        params = ()

        # If search parameters are provided, modify the query
        if search_field and search_value:
            query += " WHERE {} LIKE %s".format(search_field)
            params = ('%' + search_value + '%',)
        
        cursor.execute(query, params)
        books = cursor.fetchall()
        
        return render_template("admin.html", books=books)
    return redirect(url_for('login'))

@app.route('/admin_view_book', methods=['GET'])
def admin_view_book():
    # SQL query to get book details and its type (book, periodical, audiobook)
    viewBookId = request.args.get('bookid')
    # sql_query = """
    # SELECT b.bookid, b.title, b.author, b.isbn, b.category, b.year, b.language,
    #         CASE
    #             WHEN p.bookid IS NOT NULL THEN 'Periodical'
    #             WHEN a.bookid IS NOT NULL THEN 'Audiobook'
    #             ELSE 'Book'
    #         END AS book_type,
    #         a.audioformat
    # FROM book b
    # LEFT JOIN periodical p ON b.bookid = p.bookid
    # LEFT JOIN audiobook a ON b.bookid = a.bookid
    # WHERE b.bookid = %s
    # """

    book = dict().fromkeys(['bookid', 'title', 'author', 'isbn', 'category', 'year', 'language', 'book_type', 'audioformat'], None)
    retrieved_book = library_tree.search(int(viewBookId))
    if retrieved_book:
        book['bookid'] = retrieved_book.bookid
        book['title'] = retrieved_book.title
        book['author'] = retrieved_book.author
        book['isbn'] = retrieved_book.isbn
        book['category'] = retrieved_book.category
        book['year'] = retrieved_book.year
        book['language'] = retrieved_book.language
        if type(retrieved_book) is AudioBook: 
            book['book_type'] = "Audiobook"
            book['audioformat'] = retrieved_book.audio_format
        elif type(retrieved_book) is Periodical: book['book_type'] = "Periodical"
        else: book['book_type'] = "Book"

    return render_template('adminviewbook.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            category = request.form['category']
            year = request.form['year'] + '-01-01'
            language = request.form['language']
            book_type = request.form['type']
            
            cursor.execute('INSERT INTO book (title, author, isbn, category, year, language) VALUES (%s, %s, %s, %s, %s, %s)',
                        (title, author, isbn, category, year, language))
            db.commit()
            
            book_id = cursor.lastrowid
            
            if book_type == 'audio':
                audio_format = request.form['audio_format']
                cursor.execute('INSERT INTO audiobook (bookid, audioformat) VALUES (%s, %s)', (book_id, audio_format))
            elif book_type == 'periodical':
                cursor.execute('INSERT INTO periodical (bookid) VALUES (%s)', (book_id,))
            db.commit()
            
            return redirect(url_for('admin'))
        return render_template('add_book.html')
    return redirect(url_for('login'))

@app.route('/edit_book/<int:bookid>', methods=['GET', 'POST'])
def edit_book(bookid):
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            category = request.form['category']
            year = request.form['year'] + '-01-01'
            language = request.form['language']
            book_type = request.form['type']
            
            cursor.execute('UPDATE book SET title=%s, author=%s, isbn=%s, category=%s, year=%s, language=%s WHERE bookid=%s',
                        (title, author, isbn, category, year, language, bookid))
            
            # Check current type and remove old type entry
            cursor.execute('SELECT * FROM audiobook WHERE bookid=%s', (bookid,))
            audiobook = cursor.fetchone()
            cursor.execute('SELECT * FROM periodical WHERE bookid=%s', (bookid,))
            periodical = cursor.fetchone()
            
            if audiobook and book_type != 'audio':
                cursor.execute('DELETE FROM audiobook WHERE bookid=%s', (bookid,))
            elif periodical and book_type != 'periodical':
                cursor.execute('DELETE FROM periodical WHERE bookid=%s', (bookid,))
            
            # Insert or update new type entry
            if book_type == 'audio':
                audio_format = request.form['audio_format']
                if audiobook:
                    cursor.execute('UPDATE audiobook SET audioformat=%s WHERE bookid=%s', (audio_format, bookid))
                else:
                    cursor.execute('INSERT INTO audiobook (bookid, audioformat) VALUES (%s, %s)', (bookid, audio_format))
            elif book_type == 'periodical':
                if periodical:
                    pass
                else:
                    cursor.execute('INSERT INTO periodical (bookid) VALUES (%s)', (bookid,))
            
            db.commit()
            return redirect(url_for('admin'))
        
        cursor.execute('SELECT * FROM book WHERE bookid=%s', (bookid,))
        book = cursor.fetchone()
        
        # Determine book type
        cursor.execute('SELECT * FROM audiobook WHERE bookid=%s', (bookid,))
        audiobook = cursor.fetchone()
        cursor.execute('SELECT * FROM periodical WHERE bookid=%s', (bookid,))
        periodical = cursor.fetchone()
        
        if audiobook:
            book['type'] = 'audio'
            book['audio_format'] = audiobook['audioformat']
        elif periodical:
            book['type'] = 'periodical'
        else:
            book['type'] = 'book'
        
        return render_template('edit_book.html', book=book)
    return redirect(url_for('login'))

@app.route('/admin/delete_book/<int:bookid>', methods=['GET'])
def delete_book(bookid):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor.execute('DELETE FROM audiobook WHERE bookid=%s', (bookid,))
        cursor.execute('DELETE FROM periodical WHERE bookid=%s', (bookid,))
        cursor.execute('DELETE FROM book WHERE bookid = %s', (bookid,))
        db.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/borrowers')
def borrowers():
    if 'loggedin' in session and session['role'] == 'admin':
        query = "SELECT borrowerid, firstname, lastname, email FROM borrower WHERE email != 'admin@admin.com'"
        cursor.execute(query)
        borrowers = cursor.fetchall()
        return render_template('borrowers.html', borrowers=borrowers)
    return redirect(url_for('login'))

# Route for viewing details of a specific borrower
@app.route('/view_borrower/<int:borrowerid>')
def view_borrower(borrowerid):
    if 'loggedin' in session and session['role'] == 'admin':
        # Fetch borrower details
        query_borrower = "SELECT * FROM borrower WHERE borrowerid = %s"
        cursor.execute(query_borrower, (borrowerid,))
        borrower = cursor.fetchone()
        
        # Fetch borrowed books by the borrower
        query_borrowed_books = """
            SELECT bor.borrowedid, bor.bookid, bor.borrowdate, bor.duedate, bor.returndate,
                b.title
            FROM borrowed bor
            JOIN book b ON bor.bookid = b.bookid
            LEFT JOIN fine f ON bor.borrowedid = f.borrowedid
            WHERE bor.borrowerid = %s
            AND f.fineid IS NULL;
        """
        cursor.execute(query_borrowed_books, (borrowerid,))
        borrowed_books = cursor.fetchall()
        
        borrower['borrowed_books'] = borrowed_books
        return render_template('viewborrower.html', borrower=borrower)
    return redirect(url_for('login'))
    

@app.route('/apply_fine/<int:borrowedid>/<int:borrowerid>', methods=['GET', 'POST'])
def apply_fine(borrowedid, borrowerid):
    if 'loggedin' in session and session['role'] == 'admin':
        fine_amount = random.randint(10, 20)
    
        query_apply_fine = "INSERT INTO fine (borrowedid, status, amount) VALUES (%s, 'unpaid', %s)"
        cursor.execute(query_apply_fine, (borrowedid, fine_amount))
        db.commit()
        
        
        # Redirect back to the borrower details page after applying fine
        return redirect(url_for('view_borrower', borrowerid=borrowerid))
    return redirect(url_for('login'))


@app.route('/borrower_fines')
def borrower_fines():
    if 'loggedin' in session and session['role'] == 'admin':
        # Fetch fines with borrower details
        query_fines = """
            SELECT f.fineid, b.borrowerid, bo.firstname, bo.lastname, f.amount, f.status
            FROM fine f
            JOIN borrowed b ON f.borrowedid = b.borrowedid
            JOIN borrower bo ON b.borrowerid = bo.borrowerid
            WHERE bo.borrowerid != 1
        """
        cursor.execute(query_fines)
        fines = cursor.fetchall()
        
        return render_template('borrowerfines.html', fines=fines)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
    os.execv(__file__, sys.argv)

