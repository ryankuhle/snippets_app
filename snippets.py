import logging
import argparse

# Argument format when calling script
# type (put, get), name (name of snippet), snippet (content of snippet)
# Use positional rather than optional arguments
# python3 snippets.py put list "A sequence of things - created using []"

# Set the log output file
logging.basicConfig(filename="snippets.log",level=logging.DEBUG)

def put(name, snippet):
    """
    put
    Store a snippet with an associated name.
    Returns the name and the snippet.
    """
    # Logs the error
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    
    # Returns the name and snippet
    return name, snippet
    
def get(name):
    """
    get
    Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
    
def main():
    """
    main
    """
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args()
    
if __name__ == "__main__":
    main()