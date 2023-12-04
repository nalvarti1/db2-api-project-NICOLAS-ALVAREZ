from http.client import HTTPException
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from sqlalchemy import or_


from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookWriteDTO,
    BookUpdateDTO,
    ClientReadDTO,
    ClientWriteDTO,
    ClientUpdateDTO
    
)
from app.models import Author, Book, Client
from app.repositories import (
    AuthorRepository,
    BookRepository,
    ClientRepository,
    provide_authors_repo,
    provide_books_repo,
    provide_clients_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @post(dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    #En caso de no encontrar la id del autor da un mensaje de error
    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
         return authors_repo.get(author_id)
        except:
            raise HTTPException(
                status_code=404,
                detail="El autor no existe" 
            )
    
    #Se obtiene un autor utilizando el repositorio de autores, actualiza datos del autor y luego los guarda en el repositorio
    #En caso de no encontrarlo da un mensaje de error
    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository) -> Author:
        try:
            author = authors_repo.get(author_id)
            author = data.update_instance(author)
            return authors_repo.update(author)
        except:
            raise HTTPException(
                status_code=404,
                detail="El autor no existe" 
            )


class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        return books_repo.list()

    @post(dto=BookWriteDTO)
    async def create_book(self, data: Book, books_repo: BookRepository) -> Book:
        return books_repo.add(data)
    
    #En caso de no encontrar la id del libro da un mensaje de error
    @get('/{book_id:int}', return_dto=BookReadDTO)  
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
        
        try:
            book = books_repo.get(book_id)
            return book
        except:
            raise HTTPException(
                status_code=404,
                detail="El libro no existe" 
            )
            
    #Se obtiene un libro utilizando el repositorio de libros, actualiza datos del libro y luego los guarda en el repositorio
    #En caso de no encontrarlo da un mensaje de error
    @patch('/{book_id:int}', dto=BookUpdateDTO)  
    async def update_book(self, book_id: int, data: DTOData[Book], books_repo: BookRepository) -> Book:
       
        try:
            book = books_repo.get(book_id)
            book = data.update_instance(book)
            return books_repo.update(book)
        except:
            raise HTTPException(
                status_code=404,
                detail="El libro no existe" 
            )
    
    #Consulta a la base de datos que busque un libro que coincida con la busqueda, se ejecuta y obtiene todos los resultados
    #Si hay error en la busqueda devuelve un mensaje
    @get("/search", return_dto=BookReadDTO)
    async def search_books_by_title(self, title: str, books_repo: BookRepository) -> list[Book]:
        
        try:
            # Utiliza la sesión de SQLAlchemy para obtener la consulta
            query = books_repo.session.query(Book).filter(or_(Book.title.ilike(f"%{title}%")))
            result = query.all()
            
            return result
        except Exception as e:
            print(f"Error during book search: {e}")
            raise HTTPException(
                status_code=404,
                detail="No se encontraron libros con el título proporcionado",
            )



class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = ClientReadDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()

    @post(dto=ClientWriteDTO,use_default_session=True)
    async def create_client(self, data: Client, clients_repo: ClientRepository) -> Client:
        return clients_repo.add(data)
    
    @get('/{client_id:int}', return_dto=ClientReadDTO)
    async def get_client(self, client_id: int, clients_repo: ClientRepository) -> Client:

        client = clients_repo.get(client_id)
        return client
    
    
    @patch('/{client_id:int}', dto=ClientUpdateDTO)
    async def update_client(self, client_id: int, data: DTOData[Client], clients_repo: ClientRepository) -> Client:

        try:
            client = clients_repo.get(client_id)
            client = data.update_instance(client)
            return clients_repo.update(client)
        except:
            raise HTTPException(
                status_code=404,
                detail="El cliente no existe"
            )
        



# class ClientController(Controller):

#     path = "/clients"
#     tags = ["client"]
#     return_dto = ClientReadDTO
    
#     dependencies = {
#         "clients_repo": Provide(provide_clients_repo)
#     }

#     @get(sync_to_thread=False)
#     def get_clients(self, clients_repo: ClientRepository) -> list[Client]:
#         return clients_repo.get_all()

#     @post(dto=ClientWriteDTO,sync_to_thread=False) 
#     def create_client(self, client: Client, clients_repo: ClientRepository)-> Client:
#         return clients_repo.add(client)