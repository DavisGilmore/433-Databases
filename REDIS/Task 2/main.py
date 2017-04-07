import redis


conn = redis.Redis()


def add_book(title, author, isbn, num_pages):
    if conn.sismember('books:isbn', isbn):
        return 0
    conn.sadd('books:isbn', isbn)
    conn.hmset('books:isbn:' + isbn, {'Title': title, 'Author': author, 'NumPages': num_pages})
    conn.sadd('books:title', title)
    conn.sadd('books:title:' + title, isbn)
    conn.sadd('books:author', author)
    conn.sadd('books:author:' + author, isbn)
    return 1


def edit_book(title, author, isbn, num_pages):
    if conn.sismember('books:isbn', isbn):
        old_title = conn.hget('books:isbn:' + isbn, 'Title')
        old_author = conn.hget('books:isbn:' + isbn, 'Author')
        conn.hmset('books:isbn:' + isbn, {'Title': title, 'Author': author, 'NumPages': num_pages})
        conn.srem('books:title:' + old_title, isbn)
        if not conn.smembers('books:title:' + old_title):
            conn.srem('books:title', old_title)
        conn.sadd('books:title', title)
        conn.sadd('books:title:' + title, isbn)
        conn.srem('books:author:' + old_author, isbn)
        if not conn.smembers('books:author:' + old_author):
            conn.srem('books:author', old_author)
        conn.sadd('books:author', author)
        conn.sadd('books:author:' + author, isbn)
        return 1
    return 0


def delete_book(isbn):
    if conn.sismember('books:isbn', isbn):
        conn.srem('books:isbn', isbn)
        book = [isbn]
        book += conn.hmget('books:isbn:' + isbn, ['Title', 'Author', 'NumPages'])
        conn.hdel('books:isbn:' + isbn, 'Title', 'Author', 'NumPages')
        title = book[2]
        conn.srem('books:title:' + title, isbn)
        if not conn.smembers('books:title:' + title):
            conn.srem('books:title', title)
        author = book[3]
        conn.srem('books:author:' + author, isbn)
        if not conn.smembers('books:author:' + author):
            conn.srem('books:author', author)
        return book
    return 0


def get_book(isbn):
    if conn.sismember('books:isbn', isbn):
        book = [isbn]
        book += conn.hmget('books:isbn:' + isbn, ['Title', 'Author', 'NumPages'])
        return book
    return 0


def get_book_by_title(title):
    if conn.sismember('books:title', title):
        isbns = conn.smembers('books:title:' + title)
        books = []
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + isbn, ['Title', 'Author', 'NumPages'])
            books.insert(0, book)
        return books
    return 0


def get_book_by_author(author):
    if conn.sismember('books:author', author):
        isbns = conn.smembers('books:author:' + author)
        books = []
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + isbn, ['Title', 'Author', 'NumPages'])
            books.insert(0, book)
        return books
    return 0


def add_borrower(name, username, phone):
    if conn.sismember('borrowers:username', username):
        return 0
    conn.sadd('borrowers:username', username)
    conn.hmset('borrowed:booksOut', {username: 0})
    conn.hmset('borrowers:username:' + username, {'Name': name, 'Phone': phone})
    conn.sadd('borrowers:name', name)
    conn.sadd('borrowers:name:' + name, username)
    return 1


def edit_borrower(name, username, phone):
    if conn.sismember('borrowers:username', username):
        old_name = conn.hget('borrowers:username:' + username, 'Name')
        conn.hmset('borrowers:username:' + username, {'Name': name, 'Phone': phone})
        conn.srem('borrowers:name:' + old_name, username)
        if not conn.smembers('borrowers:name:' + old_name):
            conn.srem('borrowers:name', old_name)
        conn.sadd('borrowers:name', name)
        conn.sadd('borrowers:name:' + name, username)
        return 1
    return 0


def delete_borrower(username):
    if conn.sismember('borrowers:username', username):
        conn.srem('borrowers:username', username)
        conn.hdel('borrowed:booksOut', username)
        borrower = [username]
        borrower += conn.hmget('borrowers:username:' + username, ['Name', 'Phone'])
        conn.hdel('borrowers:username:' + username, 'Name', 'Phone')
        name = borrower[2]
        conn.srem('borrowers:name:' + name, username)
        if not conn.smembers('borrowers:name:' + name):
            conn.srem('borrowers:name', name)
        return borrower
    return 0


def get_borrower(username):
    if conn.sismember('borrowers:username', username):
        borrower = [username]
        borrower += conn.hmget('borrowers:username:' + username, ['Name', 'Phone'])
        return borrower
    return 0


def get_borrower_by_name(name):
    if conn.sismember('borrowers:name', name):
        username = conn.smembers('borrowers:name:' + name)
        borrowers = []
        for user in username:
            borrower = [user]
            borrower += conn.hmget('borrowers:username:' + user, ['Name', 'Phone'])
            borrowers.insert(0, borrower)
        return borrowers
    return 0


def checkout(username, isbn):
    if conn.sismember('borrowers:username', username) and conn.sismember('books:isbn', isbn):
        if conn.sismember('borrowed:isbn', isbn):
            return 0
        conn.sadd('borrowed:isbn', isbn)
        conn.hincrby('borrowed:booksOut', username)
        conn.hmset('borrowed:out', {isbn: username})
        return 1
    return 0


def checkin(username, isbn):
    if conn.sismember('borrowers:username', username) and conn.sismember('books:isbn', isbn):
        if conn.sismember('borrowed:isbn', isbn):
            conn.srem('borrowed:isbn', isbn)
            conn.hincrby('borrowed:booksOut', username, -1)
            conn.hdel('borrowed:out', isbn)
            return 1
        return 0
    return 0


def books_borrowed(username):
    if conn.sismember('borrowers:username', username):
        return conn.hget('borrowed:booksOut', username)
    return 0
