from abc import ABC, abstractmethod
from dto import Prestito, PrestitoDettaglio
from datetime import date

# Interfaccia DAO astratta
class PrestitoDAOInterface(ABC):

    @abstractmethod
    def assegna_prestito(self, id_utente: int, id_libro: int, id_biblioteca: int, id_bibliotecario: int, data_prevista: date) -> int:
        pass

    @abstractmethod
    def get_by_id(self, id_prestito: int) -> Prestito | None:
        pass

    @abstractmethod
    def get_dettaglio_by_id(self, id_prestito: int) -> PrestitoDettaglio | None:
        pass

    @abstractmethod
    def get_by_id_utente(self, id_utente: int) -> list[Prestito]:
        pass

    @abstractmethod
    def get_dettagli_by_id_utente(self, id_utente: int) -> list['PrestitoDettaglio']:
        pass