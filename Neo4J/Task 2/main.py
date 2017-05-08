import neo4j.v1
from neo4j.v1 import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", "password"))
ses = driver.session()


def add_book(title, author, isbn, num_pages):
	ses.run(
		"CREATE (b:Book { title: {title} , "
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