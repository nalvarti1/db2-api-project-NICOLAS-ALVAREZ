from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Author, Book,Client


class AuthorReadDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class AuthorReadFullDTO(SQLAlchemyDTO[Author]):
    pass


class AuthorWriteDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class AuthorUpdateDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)


class BookReadDTO(SQLAlchemyDTO[Book]):
    pass


class BookWriteDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author"})


class BookUpdateDTO(SQLAlchemyDTO[Book]): 
    config = SQLAlchemyDTOConfig(exclude={"id", "author"}, partial=True)


class ClientReadDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig()


class ClientReadFullDTO(SQLAlchemyDTO[Client]):
    pass


class ClientWriteDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id"})

class ClientUpdateDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)