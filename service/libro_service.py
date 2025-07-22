from repository import LibroDAOInterface
from dto import Libro

class LibroService():

    def __init__(self, libro_dao: LibroDAOInterface) -> None:
        self._dao = libro_dao

    def recupera_libro(self, id_libro: int) -> Libro | None:
        return self._dao.get_by_id(id_libro)
    
    def recupera_libri(self) -> list['Libro']:
        return self._dao.get_all()