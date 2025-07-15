from abc import ABC, abstractmethod
from dto import Libro

# Interfaccia DAO astratta
class LibroDAOInterface(ABC):

    @abstractmethod
    def create(self, libro: Libro) -> int:
        """Crea un nuovo libro e restituisce l'ID generato"""
        pass

    @abstractmethod
    def get_by_id(self, id_libro: int) -> Libro | None:
        """Recupera un libro per ID"""
        pass

    @abstractmethod
    def get_all(self) -> list[Libro]:
        """Recupera tutti i libri"""
        pass

    @abstractmethod
    def update(self, libro: Libro) -> bool:
        """Aggiorna un libro esistente"""
        pass

    @abstractmethod
    def delete(self, id_libro: int) -> bool:
        """Elimina un libro per ID"""
        pass
