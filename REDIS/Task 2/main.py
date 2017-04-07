import redis


conn = redis.Redis()


def add_book(title, author, isbn, num_pages):
    if conn.sismember('books:isbn', isbn):
        return 0
    conn.sadd('books:isbn', isbn)
    conn.hmset('books:isbn:' + str(isbn), {'Title': title, 'Author': author, 'NumPages': num_pages})
    conn.sadd('books:title', title)
    conn.sadd('books:title:' + str(title), isbn)
    conn.sadd('books:author', author)
    conn.sadd('books:author:' + str(author), isbn)
    conn.sadd('books:number_pages', num_pages)
    conn.sadd('books:number_pages:' + str(num_pages), isbn)
    return 1


def edit_book(title, author, isbn, num_pages):
    if conn.sismember('books:isbn', isbn):
        old_title = conn.hget('books:isbn:' + str(isbn), 'Title')
        old_author = conn.hget('books:isbn:' + str(isbn), 'Author')
        old_num_pages = conn.hget('books:isbn:' + str(isbn), 'NumPages')
        conn.hmset('books:isbn:' + str(isbn), {'Title': title, 'Author': author, 'NumPages': num_pages})
        conn.srem('books:title:' + str(old_title), isbn)
        if not conn.smembers('books:title:' + str(old_title)):
            conn.srem('books:title', old_title)
        conn.sadd('books:title', title)
        conn.sadd('books:title:' + str(title), isbn)
        conn.srem('books:author:' + str(old_author), isbn)
        if not conn.smembers('books:author:' + str(old_author)):
            conn.srem('books:author', old_author)
        conn.sadd('books:author', author)
        conn.sadd('books:author:' + str(author), isbn)
        conn.srem('books:number_pages:' + str(old_num_pages), isbn)
        if not conn.smembers('books:number_pages:' + str(old_num_pages)):
            conn.srem('books:number_pages', old_num_pages)
        conn.sadd('books:number_pages', num_pages)
        conn.sadd('books:number_pages:' + str(num_pages), isbn)
        return 1
    return 0


def delete_book(isbn):
    if conn.sismember('books:isbn', isbn):
        checkin(isbn)
        conn.srem('books:isbn', isbn)
        book = [isbn]
        book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
        conn.hdel('books:isbn:' + str(isbn), 'Title', 'Author', 'NumPages')
        title = book[1]
        conn.srem('books:title:' + str(title), isbn)
        if not conn.smembers('books:title:' + str(title)):
            conn.srem('books:title', title)
        author = book[2]
        conn.srem('books:author:' + str(author), isbn)
        if not conn.smembers('books:author:' + str(author)):
            conn.srem('books:author', author)
        num_pages = book[3]
        conn.srem('books:number_pages:' + str(num_pages), isbn)
        if not conn.smembers('books:number_pages:' + str(num_pages)):
            conn.srem('books:number_pages', num_pages)
        return book
    return 0


def get_book(isbn):
    if conn.sismember('books:isbn', isbn):
        book = [isbn]
        book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
        return book
    return 0


def get_book_by_title(title):
    if conn.sismember('books:title', title):
        isbns = conn.smembers('books:title:' + str(title))
        books = []
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
            books.insert(0, book)
        return books
    return 0


def get_book_by_author(author):
    if conn.sismember('books:author', author):
        isbns = conn.smembers('books:author:' + str(author))
        books = []
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
            books.insert(0, book)
        return books
    return 0


def sort_books_isbn():
    sorted = conn.sort('books:isbn', alpha=True)
    results = []
    for isbn in sorted:
        book = [isbn]
        book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
        results.insert(len(results), book)
    return results


def sort_books_title():
    sorted = conn.sort('books:title', alpha=True)
    results = []
    for title in sorted:
        isbns = conn.smembers('books:title:' + str(title))
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
            results.insert(len(results), book)
    return results



def sort_books_author():
    sorted = conn.sort('books:author', alpha=True)
    results = []
    for author in sorted:
        isbns = conn.smembers('books:author:' + str(author))
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
            results.insert(len(results), book)
    return results


def sort_books_number_pages():
    sorted = conn.sort('books:number_pages')
    results = []
    for num_pages in sorted:
        isbns = conn.smembers('books:number_pages:' + str(num_pages))
        for isbn in isbns:
            book = [isbn]
            book += conn.hmget('books:isbn:' + str(isbn), ['Title', 'Author', 'NumPages'])
            results.insert(len(results), book)
    return results


def add_borrower(name, username, phone):
    if conn.sismember('borrowers:username', username):
        return 0
    conn.sadd('borrowers:username', username)
    conn.hmset('borrowed:booksOut', {username: 0})
    conn.hmset('borrowers:username:' + str(username), {'Name': name, 'Phone': phone})
    conn.sadd('borrowers:name', name)
    conn.sadd('borrowers:name:' + str(name), username)
    return 1


def edit_borrower(name, username, phone):
    if conn.sismember('borrowers:username', username):
        old_name = conn.hget('borrowers:username:' + str(username), 'Name')
        conn.hmset('borrowers:username:' + str(username), {'Name': name, 'Phone': phone})
        conn.srem('borrowers:name:' + str(old_name), username)
        if not conn.smembers('borrowers:name:' + str(old_name)):
            conn.srem('borrowers:name', old_name)
        conn.sadd('borrowers:name', name)
        conn.sadd('borrowers:name:' + str(name), username)
        return 1
    return 0


def delete_borrower(username):
    if conn.sismember('borrowers:username', username):
        conn.srem('borrowers:username', username)
        conn.hdel('borrowed:booksOut', username)
        borrower = [username]
        borrower += conn.hmget('borrowers:username:' + str(username), ['Name', 'Phone'])
        conn.hdel('borrowers:username:' + str(username), 'Name', 'Phone')
        name = borrower[1]
        conn.srem('borrowers:name:' + str(name), username)
        if not conn.smembers('borrowers:name:' + str(name)):
            conn.srem('borrowers:name', name)
        books = conn.smembers('borrowed:username:' + str(username))
        for isbn in books:
            checkin(isbn)
        return borrower
    return 0


def get_borrower(username):
    if conn.sismember('borrowers:username', username):
        borrower = [username]
        borrower += conn.hmget('borrowers:username:' + str(username), ['Name', 'Phone'])
        return borrower
    return 0


def get_borrower_by_name(name):
    if conn.sismember('borrowers:name', name):
        username = conn.smembers('borrowers:name:' + str(name))
        borrowers = []
        for user in username:
            borrower = [user]
            borrower += conn.hmget('borrowers:username:' + str(user), ['Name', 'Phone'])
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
        conn.sadd('borrowed:username:' + str(username), isbn)
        return 1
    return 0


def checkin(isbn):
    if conn.sismember('books:isbn', isbn) and conn.sismember('borrowed:isbn', isbn):
        username = conn.hget('borrowed:out', isbn)
        conn.srem('borrowed:isbn', isbn)
        conn.hincrby('borrowed:booksOut', username, -1)
        conn.hdel('borrowed:out', isbn)
        conn.srem('borrowed:username:' + str(username), isbn)
        return 1
    return 0


def books_borrowed(username):
    if conn.sismember('borrowers:username', username):
        return conn.hget('borrowed:booksOut', username)
    return 0


def borrowed_by(isbn):
    if conn.sismember('books:isbn', isbn) and conn.sismember('borrowed:isbn', isbn):
        return conn.hget('borrowed:out', isbn)
    return 0
