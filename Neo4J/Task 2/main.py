import neo4j.v1
from neo4j.v1 import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", "password"))
ses = driver.session()


def add_book(title, author, isbn, num_pages):
	return ses.run(
		"CREATE (b:Book { title: {title}, "
		"author: {author}, "
		"isbn: {isbn}, "
		"num_pages: {num_pages}})",
		{
			"title": title,
			"author": author,
			"isbn": isbn,
			"num_pages": num_pages
		}
		)


def del_book(isbn):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"DELETE b",
		{"isbn": isbn}
	)


def edit_book_isbn(isbn, new_isbn):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"SET b.isbn = {new_isbn}",
		{"isbn": isbn, "new_isbn": new_isbn}
	)


def edit_book_title(isbn, new_title):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"SET b.title = {new_title}",
		{"isbn": isbn, "new_title": new_title}
	)


def edit_book_pages(isbn, new_num_pages):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"SET b.num_pages = {new_num_pages}",
		{"isbn": isbn, "new_num_pages": new_num_pages}
	)


def edit_book_del_author(isbn, author):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"SET b.author = FILTER(x IN b.author WHERE x <> {author}",
		{"isbn": isbn, "author": author}
	)


def edit_book_add_author(isbn, author):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"SET b.author = b.author + {author}",
		{"isbn": isbn, "author": author}
	)


def search_book_isbn(isbn):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"RETURN b",
		{"isbn": isbn}
	)


def search_book_title(title):
	return ses.run(
		"MATCH (b:Book { title: {title}})"
		"RETURN b",
		{"title": title}
	)


def search_book_author(author):
	return ses.run(
		"MATCH (b:Book { author: {author}})"
		"RETURN b",
		{"author": author}
	)


def sort_book_isbn():
	return ses.run(
		"MATCH (b:Book)"
		"RETURN b"
		"ORDER BY b.isbn"
	)


def sort_book_title():
	return ses.run(
		"MATCH (b:Book)"
		"RETURN b"
		"ORDER BY b.title"
	)


def sort_book_author():
	return ses.run(
		"MATCH (b:Book)"
		"RETURN b"
		"ORDER BY b.author"
	)


def sort_book_num_pages():
	return ses.run(
		"MATCH (b:Book)"
		"RETURN b"
		"ORDER BY b.num_pages"
	)


def add_borrower(name, username, phone):
	return ses.run(
		"CREATE (b:Borrower { name: {name},"
		"username: {username},"
		"phone: {phone}})",
		{
			"name": name,
			"username": username,
			"phone": phone
		}
	)


def del_borrower(username):
	return ses.run(
		"MATCH (b:Borrower { username: {username}})"
		"DELETE b",
		{"username": username}
	)


def edit_borrower_name(username, new_name):
	return ses.run(
		"MATCH (b:Borrower { username: {username}})"
		"SET b.name = {name}",
		{"username": username, "name": new_name}
	)


def edit_borrower_username(username, new_username):
	return ses.run(
		"MATCH (b:Borrower { username: {username}})"
		"SET b.username = {username}",
		{"username": username, "name": new_username}
	)


def edit_borrower_phone(username, new_phone):
	return ses.run(
		"MATCH (b:Borrower { username: {username}})"
		"SET b.phone = {phone}",
		{"username": username, "name": new_phone}
	)


def search_borrower_username(username):
	return ses.run(
		"MATCH (b:Borrower { username: {username}})"
		"RETURN b",
		{"username": username}
	)


def search_borrower_name(name):
	return ses.run(
		"MATCH (b:Borrower { name: {name}})"
		"RETURN b",
		{"name": name}
	)


def checkout_book(username, isbn):
	return ses.run(
		"MATCH (r:Borrower { username: {username}}),"
		"(b:Book { isbn: {isbn}})"
		"CREATE (r)-[:Borrowed]->(b)",
		{"username": username, "isbn": isbn}
	)


def checkin_book(isbn):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"DELETE (:Borrower)-[:Borrowed]->(b)",
		{"isbn": isbn}
	)


def book_status(isbn):
	return ses.run(
		"MATCH (b:Book { isbn: {isbn}})"
		"MATCH (r:Borrower)-[:Borrowed]->(b)"
		"RETURN r",
		{"isbn": isbn}
	)


def books_borrower(username):
	return ses.run(
		"MATCH (r:Borrower { username: {username}})"
		"MATCH (r)-[:Borrowed]->()"
		"RETURN COUNT(*)",
		{"username": username}
	)


def main():
    while True:
        print("Welcome to the Library! What would you like to do?")
        cmd = input(":")
        if cmd.lower() == "add book":
            print("What is the book ISBN?")
            isbn = input(":")
            print("What is the book title?")
            title = input(":")
            print("How many authors are there?")
            num = input(":")
            authors = []
            try:
                 n = int(num)
            except:
                print("Error not a number!")
                continue
            while n > 0:
                print("Input author")
                authors.append(input(":"))
                n = n - 1
            print("How many pages are there?")
            pages = input(":")
            if add_book(title, authors, isbn, pages) :
                print("operation successful")
            else :
                print("operation failed")
        elif cmd.lower() == "del book":
            print("What is the ISBN?")
            isbn = input(":")
            if del_book(isbn):
                print("operation successful")
            else:
                print("operation failed")
        elif cmd.lower() == "edit book":
            print("What is the ISBN?")
            isbn = input(":")
            print("Would you like to remove an author?(Y/N)")
            cmd = input(":")
            if cmd.lower() == "y" :
                print("Which author would you like to remove?")
                author = input(":")
                if edit_book_del_author(isbn, author) :
                    print("operation successful")
                else :
                    print("operation failed")
            else :
                print("What attribute would you like to edit?(isbn, title, author, numpages")
                cmd = input(":")
                if cmd.lower() == "isbn":
                    print("What is the new isbn?")
                    nisbn= input(":")
                    if edit_book_isbn(isbn, nisbn):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "title":
                    print("What is the new title?")
                    title = input(":")
                    if edit_book_title(isbn, title):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "numpages":
                    print("What is the new number of pages?")
                    pages = input(":")
                    if edit_book_pages(isbn, pages):
                        print("operation successful")
                    else:
                        print("operation failed")
                elif cmd.lower() == "author":
                    print("Who is the new author?")
                    author = input(":")
                    if edit_book_add_author(isbn, author):
                        print("operation successful")
                    else:
                        print("operation failed")
                else:
                    print("Not an option")
        elif cmd.lower() == "search books" :
            print("What would you like to search by?(isbn, title, author)")
            cmd = input(":")
            print("What is your search term?")
            search = input(":")
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
            cmd = input(":")
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
            user = input(":")
            print("What is the borrower's name?")
            name = input(":")
            print("What is the borrower's phone number?")
            phone = input(":")
            if add_borrower(name, user, phone):
                print("operation succesful")
            else :
                print("operation failed")
        elif cmd.lower() == "del borrower" :
            print("What is the username of the borrower to be deleted?")
            user = input(":")
            if del_borrower(user):
                print("operation succesful")
            else :
                print("operation failed")
        elif cmd.lower() == "edit borrower" :
            print("What username would you like to update?")
            username = input(":")
            print("What attribute would you like to update?(name, username, phone)")
            cmd = input(":")
            if cmd.lower() == "name" :
                print("What is the new name?")
                name = input(":")
                if edit_borrower_name(username, name):
                    print("operation succesful")
                else:
                    print("operation failed")
            elif cmd.lower() == "username":
                print("What is the new username?")
                nuser = input(":")
                if edit_borrower_username(username, nuser):
                    print("operation succesful")
                else:
                    print("operation failed")
            elif cmd.lower() == "phone":
                print("What is the new phone number?")
                phone = input(":")
                if edit_borrower_phone(username, phone):
                    print("operation succesful")
                else:
                    print("operation failed")
            else :
                print("invalid attribute")
        elif cmd.lower() == "search borrowers" :
            print("What would you like to search on?(username, name)")
            cmd = input(":")
            print("What is your search term?")
            search = input(":")
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
            username = input(":")
            print("What is the ISBN?")
            isbn = input(":")
            if checkout_book(username, isbn):
                print("operation succesful")
            else:
                print("operation failed")
        elif cmd.lower() == "checkin" :
            print("What is the ISBN?")
            isbn = input(":")
            if checkin_book(isbn):
                print("operation succesful")
            else:
                print("operation failed")
        elif cmd.lower() == "book status" :
            print("What ISBN would you like to check?")
            isbn = input(":")
            status = book_status(isbn)
            if status == 0:
                print("operation failed")
                continue
            if status == -1:
                print(str(isbn) + " is not currently checked out")
            else:
                print(str(isbn) + " is currently checked out to \'" + status + "\'")
        elif cmd.lower() == "books borrowed" :
            print("What borrower would you like to view?")
            username = input(":")
            books = books_borrowed(username)
            print("User: \'" + str(username) + "\' has " + str(books) + " books checked out")
        elif cmd.lower() == "exit":
            return 0
        else :
            print("Available commands are: \'add book\', \'edit book\', \'del book\', \'search books\', \'sort books\', \'add borrower\', \'edit borrower\', \'del borrower\', \'search borrowers\', \'checkin\', \'checkout\', \'book status\', \'books borrowed\', \'exit\'")


main()
