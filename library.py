from dataclasses import dataclass


class Book:
    title: str
    author: str
    isbn: str
    is_checked_out: bool

    def __init__(
        self, title: str, author: str, isbn: str, is_checked_out: bool = False
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = is_checked_out

    def check_out(self):
        self.is_checked_out = True

    def return_book(self):
        self.is_checked_out = False

    def __str__(self) -> str:
        return (
            "title: "
            + self.title
            + " author: "
            + self.author
            + " isbn: "
            + self.isbn
            + " is_checked_out: "
            + str(self.is_checked_out)
        )

    def __repr__(self):
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r}, checked_out={self.is_checked_out})"


class Member:
    name: str
    member_id: str
    borrowed_books: list[Book]

    def __init__(
        self, name: str, member_id: str, borrowed_books: list[Book] | None = None
    ):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = borrowed_books or []

    def borrow(self, book: Book):
        self.borrowed_books.append(book)
        book.check_out()

    def return_book(self, book: Book):
        self.borrowed_books.remove(book)
        book.return_book()

    def __str__(self) -> str:
        return (
            "name: "
            + self.name
            + " member_id: "
            + self.member_id
            + " borrowed_books: "
            + str(self.borrowed_books)
        )

    def list_borrowed_books(self) -> str:
        # ToDo
        return str(self.borrowed_books)


class Library:
    books: list[Book]
    members: list[Member]

    def __init__(self):
        self.books: list[Book] = []
        self.members: list[Member] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def add_member(self, member: Member):
        self.members.append(member)

    def find_book_by_isbn(self, isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_member_by_member_id(self, member_id: str) -> Member | None:
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def checkout_book(self, isbn: str, member_id: str) -> bool:
        book: Book | None = self.find_book_by_isbn(isbn)
        if book is None:
            print("book with isbn could not be found in library.")
            return False

        if book.is_checked_out:
            print("book is already checked out.")
            return False

        member: Member | None = self.find_member_by_member_id(member_id)
        if member is None:
            print("No member with given member ID found in library.")
            return False

        member.borrow(book)
        return True

    def return_book(self, isbn: str, member_id: str) -> bool:
        book: Book | None = self.find_book_by_isbn(isbn)
        if book is None:
            print("book with isbn could not be found in library.")
            return False

        member: Member | None = self.find_member_by_member_id(member_id)
        if member is None:
            print("No member with given member ID found in library.")
            return False

        if book not in member.borrowed_books:
            print("Member did not borrow this book.")
            return False

        member.return_book(book)
        return True

    def list_available_books(self) -> list[Book]:
        available_books: list[Book] = []
        for book in self.books:
            if not book.is_checked_out:
                available_books.append(book)
        return available_books

    def __str__(self) -> str:
        return "books: " + str(self.books) + " members: " + str(self.members)


@dataclass
class Test:
    name: str
    age: int


print("test")
library = Library()

book1 = Book("1984", "George Orwell", "123")
book2 = Book("Dune", "Frank Herbert", "456")

member = Member("Alice", "001")

library.add_book(book1)
library.add_book(book2)
library.add_member(member)

library.checkout_book("123", "001")
library.checkout_book("456", "001")

library.return_book("123", "001")

print(library.list_available_books())
