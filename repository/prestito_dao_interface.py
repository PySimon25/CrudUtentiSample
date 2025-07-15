from abc import ABC, abstractmethod
from dto import Prestito
from datetime import date

# Interfaccia DAO astratta
class PrestitoDAOInterface(ABC):

    @abstractmethod
    def assegna_prestito(self, prestito: Prestito) -> int:
        pass

    @abstractmethod
    def get_by_id(self, id_prestito: int) -> Prestito | None:
        pass

    @abstractmethod
    def get_by_id_utente(self, id_utente: int) -> list[Prestito]:
        pass