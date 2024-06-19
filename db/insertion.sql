INSERT INTO `book` (`author`, `title`, `isbn`, `category`, `year`, `language`) VALUES
('J.K. Rowling', 'Harry Potter and the Sorcerer Stone', '978-0747532699', 'Fantasy', '1997-06-26 00:00:00', 'English'),
('George Orwell', '1984', '978-0451524935', 'Dystopian', '1949-06-08 00:00:00', 'English'),
('J.R.R. Tolkien', 'The Hobbit', '978-0547928227', 'Fantasy', '1937-09-21 00:00:00', 'English'),
('F. Scott Fitzgerald', 'The Great Gatsby', '978-0743273565', 'Classics', '1925-04-10 00:00:00', 'English'),
('Harper Lee', 'To Kill a Mockingbird', '978-0061120084', 'Classics', '1960-07-11 00:00:00', 'English'),
('Herman Melville', 'Moby-Dick', '978-1503280786', 'Classics', '1851-10-18 00:00:00', 'English'),
('Leo Tolstoy', 'War and Peace', '978-1400079988', 'Historical Fiction', '1869-01-01 00:00:00', 'Russian'),
('Jane Austen', 'Pride and Prejudice', '978-1503290563', 'Romance', '1813-01-28 00:00:00', 'English'),
('Mark Twain', 'Adventures of Huckleberry Finn', '978-0486280615', 'Adventure', '1884-12-10 00:00:00', 'English'),
('Charles Dickens', 'Great Expectations', '978-1503280298', 'Classics', '1861-08-01 00:00:00', 'English');

INSERT INTO `periodical` (`bookid`) VALUES
(1),
(2),
(3);

INSERT INTO `audiobook` (`bookid`, `audioformat`) VALUES
(5, 'mp3'),
(6, 'mp3'),
(7, 'mp3');
(10, 'mp3');

INSERT INTO `borrower` (`firstname`, `lastname`, `email`, `password`, `role`) VALUES
('John', 'Doe', 'john.doe@example.com', 'password1', 'borrower'),
('Jane', 'Smith', 'jane.smith@example.com', 'password2', 'borrower'),
('Alice', 'Johnson', 'alice.johnson@example.com', 'password3', 'borrower'),
('Bob', 'Williams', 'bob.williams@example.com', 'password4', 'borrower'),
('Charlie', 'Brown', 'charlie.brown@example.com', 'password5', 'borrower'),
('Dave', 'Jones', 'dave.jones@example.com', 'password6', 'borrower'),
('Eve', 'Miller', 'eve.miller@example.com', 'password7', 'borrower'),
('Frank', 'Wilson', 'frank.wilson@example.com', 'password8', 'borrower'),
('Grace', 'Davis', 'grace.davis@example.com', 'password9', 'borrower'),
('Hank', 'Taylor', 'hank.taylor@example.com', 'password10', 'borrower');

INSERT INTO `borrowed` (`bookid`, `borrowerid`, `borrowdate`, `duedate`, `returndate`) VALUES
(1, 1, '2023-01-01 00:00:00', '2023-02-01 00:00:00', '2023-01-20 00:00:00'),
(2, 1, '2023-02-01 00:00:00', '2023-03-01 00:00:00', '2023-02-25 00:00:00'),
(3, 1, '2023-03-01 00:00:00', '2023-04-01 00:00:00', '2023-03-20 00:00:00'),
(5, 4, '2023-04-01 00:00:00', '2023-05-01 00:00:00', '2023-04-25 00:00:00'),
(5, 5, '2023-05-01 00:00:00', '2023-06-01 00:00:00', '2023-05-20 00:00:00'),
(5, 3, '2023-06-01 00:00:00', '2023-07-01 00:00:00', '2023-06-25 00:00:00'),
(5, 7, '2023-07-01 00:00:00', '2023-08-01 00:00:00', '2023-07-25 00:00:00'),
(5, 2, '2023-08-01 00:00:00', '2023-09-01 00:00:00', '2023-08-25 00:00:00'),
(7, 9, '2023-09-01 00:00:00', '2023-10-01 00:00:00', '2023-09-25 00:00:00'),
(10, 2, '2023-10-01 00:00:00', '2023-11-01 00:00:00', '2023-10-25 00:00:00');

INSERT INTO `fine` (`borrowedid`, `status`, `amount`) VALUES
(1, 'unpaid', 10),
(4, 'paid', 5),
(6, 'unpaid', 7),
(5, 'paid', 8),
(3, 'unpaid', 6),
(2, 'paid', 4);



