from abc import ABC, abstractmethod
from dto import Utente

# Interfaccia DAO astratta
class UtenteDAOInterface(ABC):

    @abstractmethod
    def create(self, utente: Utente) -> int:
        """Crea un nuovo utente e restituisce l'ID generato"""
        pass
        
    @abstractmethod
    def get_by_id(self, id_utente: int) -> Utente | None:
        """Recuoera un utente per ID"""
        pass

    @abstractmethod
    def get_all(self) -> list[Utente]:
        """Recupera tutti gli utenti"""
        pass

    @abstractmethod
    def update(self, utente: Utente) -> bool:
        """Aggiorna un utente esistente"""
        pass

    @abstractmethod
    def delete(self, id_utente: int) -> bool:
        """Elimina un utente per ID"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Utente | None:
        """Trova un utente per email"""
        pass
    