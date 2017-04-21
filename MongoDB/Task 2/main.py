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
    if db.books.count({'ISBN': isbn, 'Borrowed': -1}) == 0:
        usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
        for user in usernames:
            username = user.values()[0]
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
    return db.books.find().sort('ISBN', 1)


def sort_book_title():
    return db.books.find().sort('Title', 1)


def sort_book_author():
    return db.books.find().sort('Authors', 1)


def sort_book_num_pages():
    return db.books.find().sort('NumberPages', 1)


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
    db.borrowers.update_one(
        {'Username': username},
        {'$inc': {'Books': 1}}
    )
    res = db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'Borrowed': username}}
    )
    return res


def checkin_book(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
    for user in usernames:
        username = user.values()[0]
    db.books.update_one(
        {'ISBN': isbn},
        {'$set': {'Borrowed': -1}}
    )
    res = db.borrowers.update_one(
        {'Username': username},
        {'$inc': {'Books': -1}}
    )
    return res


def book_status(isbn):
    if db.books.count({'ISBN': isbn}) <= 0:
        return 0
    usernames = db.books.find({'ISBN': isbn}, {'_id': 0, 'Borrowed': 1})
    for user in usernames:
        username = user.values()[0]
    return username


def books_borrowed(username):
    if db.borrowers.count({'Username': username}) <= 0:
        return 0
    books = db.borrowers.find({'Username': username}, {'_id': 0, 'Books': 1})
    for b in books:
        number = b.values()[0]
    return number


def main():
    while True:
        print("Welcome to the Library! What would you like to do?")
        cmd = raw_input(":")
        if cmd.lower() == "add book":
            print("What is the book ISBN?")
            isbn = raw_input(":")
            print("What is the book title?")
            title = raw_input(":")
            print("How many authors are there?")
            num = raw_input(":")
            authors = []
            try:
                 n = int(num)
            except:
                print("Error not a number!")
                continue
            while n > 0:
                print("Input author")
                authors.append(raw_input(":"))
                n = n - 1
            print("How many pages are there?")
            pages = raw_input(":")
            if add_book(title, authors, isbn, pages) :
                print("operation successful")
            else :
                print("operation failed")
        elif cmd.lower() == "del book":
            print("What is the ISBN?")
            isbn = raw_input(":")
            if del_book(isbn):
                print("operation successful")
            else:
                print("operation failed")
        elif cmd.lower() == "edit book":
            print("What is the ISBN?")
            isbn = raw_input(":")
            print("Would you like to remove an attribute?(Y/N)")
            cmd = raw_input(":")
            if cmd.lower() == "y" :
                print("What attribute would you like to remove?(title, author, numpages")
                cmd = raw_input(":")
                if cmd.lower() == "title" :
                    if del_book_title(isbn):
                        print("operation successful")
                    else :
                        print("operation failed")
                elif cmd.lower() == "numpages" :
                    if del_book_title(isbn):
                        print("operation successful")
                    else :
                        print("operation failed")
                elif cmd.lower() == "author":
                    print("Which author would you like to remove?")
                    author = raw_input(":")
                    if edit_book_del_author(isbn, author) :
                        print("operation successful")
                    else :
                        print("operation failed")
                else :
                    print("Not an option")
            else :
                print("What attribute would you like to edit?(isbn, title, author, numpages")
                cmd = raw_input(":")
                if cmd.lower() == "isbn":
                    print("What is the new isbn?")
                    nisbn= raw_input(":")
                    if edit_book_isbn(isbn, nisbn):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "title":
                    print("What is the new title?")
                    title = raw_input(":")
                    if edit_book_title(isbn, title):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "numpages":
                    print("What is the new number of pages?")
                    pages = raw_input(":")
                    if edit_book_pages(isbn, pages):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "author":
                    print("Who is the new author?")
                    author = raw_input(":")
                    if edit_book_add_author(isbn, author):
                        print("operation successful")
                    else:
                        print("operation failed")
                else:
                    print("Not an option")
        elif cmd.lower() == "search books" :
            print("What would you like to search by?(isbn, title, author)")
            cmd = raw_input(":")
            print("What is your search term?")
            search = raw_input(":")
            if cmd.lower() == "isbn" :
                cursor = search_book_isbn(search)
            elif cmd.lower() == "title" :
                cursor = search_book_title(search)
            elif cmd.lower() == "author" :
                cursor = search_book_author(search)
            else :
                print("invalid search by")
                continue
            for tuple in cursor:
                print(tuple)
        elif cmd.lower() == "sort books" :
            print("Which sorted group would you like to see?(isbn, title, author, numpages)")
            cmd = raw_input(":")
            if cmd.lower() == "isbn" :
                cursor = sort_book_isbn()
            elif cmd.lower() == "title" :
                cursor = sort_book_title()
            elif cmd.lower() == "author" :
                cursor = sort_book_author()
            elif cmd.lower() == "numpages" :
                cursor = sort_book_num_pages()
            else :
                print("invalid search by")
                continue
            for tuple in cursor:
                print(tuple)
        elif cmd.lower() == "add borrower" :
            print("What is the borrower's username?")
            user = raw_input(":")
            print("What is the borrower's name?")
            name = raw_input(":")
            print("What is the borrower's phone number?")
            phone = raw_input(":")
            if add_borrower(name, user, phone):
                print("operation succesful")
            else :
                print("operation failed")
        elif cmd.lower() == "del borrower" :
            print("What is the username of the borrower to be deleted?")
            user = raw_input(":")
            if del_borrower(user):
                print("operation succesful")
            else :
                print("operation failed")
        elif cmd.lower() == "edit borrower" :
            print("What username would you like to update?")
            username = raw_input(":")
            print("What attribute would you like to update?(name, username, phone)")
            cmd = raw_input(":")
            if cmd.lower() == "name" :
                print("What is the new name?")
                name = raw_input(":")
                if edit_borrower_name(username, name):
                    print("operation succesful")
                else:
                    print("operation failed")
            elif cmd.lower() == "username":
                print("What is the new username?")
                nuser = raw_input(":")
                if edit_borrower_username(username, nuser):
                    print("operation succesful")
                else:
                    print("operation failed")
            elif cmd.lower() == "phone":
                print("What is the new phone number?")
                phone = raw_input(":")
                if edit_borrower_phone(username, phone):
                    print("operation succesful")
                else:
                    print("operation failed")
            else :
                print("invalid attribute")
        elif cmd.lower() == "search borrowers" :
            print("What would you like to search on?(username, name)")
            cmd = raw_input(":")
            print("What is your search term?")
            search = raw_input(":")
            if cmd.lower() == "username":
                cursor = search_borrower_username(search)
            elif cmd.lower() == "name":
                cursor = search_borrower_name(search)
            else:
                print("invalid search by")
                continue
            for tuple in cursor:
                print(tuple)
        elif cmd.lower() == "checkout" :
            print("What is the username?")
            username = raw_input(":")
            print("What is the ISBN?")
            isbn = raw_input(":")
            if checkout_book(username, isbn):
                print("operation succesful")
            else:
                print("operation failed")
        elif cmd.lower() == "checkin" :
            print("What is the ISBN?")
            isbn = raw_input(":")
            if checkin_book(isbn):
                print("operation succesful")
            else:
                print("operation failed")
        elif cmd.lower() == "book status" :
            print("What ISBN would you like to check?")
            isbn = raw_input(":")
            status = book_status(isbn)
            if  status == -1:
                print(str(isbn) + " is not currently checked out")
            else:
                print(str(isbn) + " is currently checked out to \'" + status + "\'")
        elif cmd.lower() == "books borrowed" :
            print("What borrower would you like to view?")
            username = raw_input(":")
            books = books_borrowed(username)
            print("User: \'" + str(username) + "\' has " + str(books) + " books checked out")
        elif cmd.lower() == "exit":
            return 0
        else :
            print("Available commands are: \'add book\', \'edit book\', \'del book\', \'search books\', \'sort books\', \'add borrower\', \'edit borrower\', \'del borrower\', \'search borrowers\', \'checkin\', \'checkout\', \'book status\', \'books borrowed\', \'exit\'")


main()
