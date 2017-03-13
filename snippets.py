"""
snippets
Notetaking program to store short clips of text.

Features to Add:
Hidden snippets
1) Maybe you don't want all your snippets to be visible in the catalog. 
Create a column hidden boolean not null default false and have the catalog 
and search functions filter their results with where not hidden. You can 
then add optional arguments to the put subcommand such as --hide, which will
set the hidden flag, and one of --show, --unhide, --no-hide, or --hide=0, 
which will reset it. (If neither flag is set, leave the hidden flag as it was.)
2) Delete snippet with confirmation
3) Date and time snippet was recorded

Bugs to Fix:
What to do if incorrect command entered.

"""

import logging
import argparse
import psycopg2

# Argument format when calling script
# type (put, get), name (name of snippet), snippet (content of snippet)
# Use positional rather than optional arguments
# python3 snippets.py put list "A sequence of things - created using []"

# Set the log output file
logging.basicConfig(filename="snippets.log",level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    put
    Store a snippet with an associated name.
    Returns the name and the snippet.
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    
    with connection, connection.cursor() as cursor:
        try:
            cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s", (name, snippet))
        
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """
    get
    Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    
    connection.commit()
    logging.debug("Snippet retrieved successfully.")
    
    if not row:
        # No snippet was found with that name
        return "404: Snippet Not Found"
        
    return row[0]
    
def catalog():
    """
    catalog
    Lists searchable keywords.
    """
    logging.info("Printing keyword catalog.")
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets order by keyword")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])

def search(string):            
    """
    search
    """
    logging.info("Searching snippets for: {!r}".format(string))
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where message like '%{}%'".format(string))
        rows = cursor.fetchall()
        for row in rows:
            print("Keyword: ", row[0], " Snippet: ", row[1])
    
def main():
    """
    main
    """
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of the snippet")
    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Catalog of snippet keywords")
    
    # Subparser for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Search snippets")
    search_parser.add_argument("string", help="Snippet search string")

    arguments = parser.parse_args()
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "search":
        string = search(**arguments)
    elif command == "catalog":
        catalog()
    
if __name__ == "__main__":
    main()