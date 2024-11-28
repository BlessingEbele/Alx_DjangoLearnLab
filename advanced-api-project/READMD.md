"""
BookListView: Lists all books.
BookDetailView: Retrieves details of a single book by ID.
BookCreateView: Allows authenticated users to create a new book.
BookUpdateView: Allows authenticated users to update an existing book.
BookDeleteView: Allows authenticated users to delete a book.
"""


### API Features for `/api/books/`

#### Filtering:
- `/api/books/?title=Book+Title`
- `/api/books/?author__name=John+Doe`
- `/api/books/?publication_year=2020`

#### Searching:
- `/api/books/?search=magic`

#### Ordering:
- `/api/books/?ordering=title`
- `/api/books/?ordering=-publication_year`

You can combine filters, searches, and ordering in a single request.
