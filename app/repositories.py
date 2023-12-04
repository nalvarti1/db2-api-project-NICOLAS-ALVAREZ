from litestar.contrib.sqlalchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import Author, Book,Client,BookCopy,Loan


class AuthorRepository(SQLAlchemySyncRepository[Author]):
    model_type = Author


async def provide_authors_repo(db_session: Session):
    return AuthorRepository(session=db_session, auto_commit=True)


class BookRepository(SQLAlchemySyncRepository[Book]):
    model_type = Book


async def provide_books_repo(db_session: Session):
    return BookRepository(session=db_session, auto_commit=True)

class ClientRepository(SQLAlchemySyncRepository[Client]):
    model_type = Client

async def provide_clients_repo(db_session: Session):
    return ClientRepository(session=db_session, auto_commit=True)

# repositories.py

class BookCopyRepository(SQLAlchemySyncRepository[BookCopy]):
    model_type = BookCopy
    

class LoanRepository(SQLAlchemySyncRepository[Loan]):   
    model_type = Loan