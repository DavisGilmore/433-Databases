import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client['library']


def add_book(title, authors, isbn, num_pages):
    if db.books.count({'ISBN': isbn}) > 0:
        return 0
    res = db.books.insert_one(
        {
            'Title': str(title),
            'Authors': authors,
            'ISBN': isbn,
            'NumberPages': num_pages,
            'Borrowed': -1
        }
    )
    return res


def del_book(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    if db.books.count({'ISBN': isbn, 'Borrowed': -1}) > 0:
        usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
        for user in usernames:
            username = user[0]
        db.borrowers.update_one(
            {'Username': username},
            {'$inc': {'Books': -1}}
        )
    return db.books.delete_one({'ISBN': isbn})


def edit_book_title(isbn, title):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'Title': title}}
    )
    return res


def edit_book_isbn(isbn, new_isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    if db.books.count({'ISBN': new_isbn}) > 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'ISBN': new_isbn}}
    )
    return res


def edit_book_pages(isbn, pages):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'NumberPages': pages}}
    )
    return res


def edit_book_add_author(isbn, author):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$push': {'Authors': author}}
    )
    return res


def edit_book_del_author(isbn, author):
    if db.books.count({'ISBN': isbn, 'Authors': author}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$pull': {'Authors': author}}
    )
    return res


def del_book_title(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$unset': {'Title': ""}}
    )
    return res


def del_book_pages(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$unset': {'NumberPages': ""}}
    )
    return res


def search_book_isbn(isbn):
    return db.books.find({'ISBN': isbn})


def search_book_title(title):
    return db.books.find({'Title': title})


def search_book_author(author):
    return db.books.find({'Authors': author})


def sort_book_isbn():
    return db.books.sort('ISBN', 1)


def sort_book_title():
    return db.books.sort('Title', 1)


def sort_book_author():
    return db.books.sort('Authors', 1)


def sort_book_num_pages():
    return db.books.sort('NumberPages', 1)


def add_borrower(name, username, phone):
    if db.borrowers.count({'Username': username}) > 0:
        return 0
    res = db.borrowers.insert_one(
        {
            'Username': username,
            'Name': name,
            'Phone': phone,
            'Books': 0
        }
    )
    return res


def del_borrower(username):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    db.books.update(
        {'Borrowed': username},
        {'$set': {'Borrowed': -1}}
    )
    res = db.borrowers.delete_one({'Username': username})
    return res


def edit_borrower_username(username, new_username):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    if db.borrowers.count({'Username': new_username}) > 0:
        return 0
    res = db.borrowers.update_one(
        {'Username': username},
        {'$set': {'Username': username}}
    )
    return res


def edit_borrower_name(username, name):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    res = db.borrowers.update_one(
        {'Username': username},
        {'$set': {'Name': name}}
    )
    return res


def edit_borrower_phone(username, phone):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    res = db.borrowers.update_one(
        {'Username': username},
        {'$set': {'Phone': phone}}
    )
    return res


def search_borrower_username(username):
    return db.borrowers.find({'Username': username})


def search_borrower_name(name):
    return db.borrowers.find({'Name': name})


def checkout_book(username, isbn):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    if db.books.count({'ISBN': isbn, 'Borrowed': -1}) <= 0:
        return 0
    res = db.borrowers.update_one(
        {'Username': username},
        {'$inc': {'Books': 1}}
    )
    res = res + db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'Borrowed': username}}
    )
    return res


def checkin_book(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
    for user in usernames:
        username = user[0]
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'Borrowed': -1}}
    )
    res = res + db.borrowers.update_one(
        {'Username': username},
        {'$inc': {'Books': -1}}
    )
    return res


def book_status(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
    for user in usernames:
        username = user[0]
    return username


def books_borrowed(username):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    books = db.books.find({'Username': username}, {'_id': 0, 'Books': 1})
    for b in books:
        book = b[0]
    return book
