from dto import Utente
import re

class UtenteBusiness:

    def __init__(self, dto: Utente) -> None:
        self._dto = dto

    # Nome
    @property
    def nome(self) -> str:
        return self._dto.nome

    @nome.setter
    def nome(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Il nome non può essere vuoto.")
        self._dto.nome = value

    # Cognome
    @property
    def cognome(self) -> str:
        return self._dto.cognome

    @cognome.setter
    def cognome(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Il cognome non può essere vuoto.")
        self._dto.cognome = value

    # Email
    @property
    def email(self) -> str:
        return self._dto.email

    @email.setter
    def email(self, value: str):
        value = value.strip().lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Email non valida.")
        self._dto.email = value

    # Telefono
    @property
    def telefono(self) -> str:
        return self._dto.telefono

    @telefono.setter
    def telefono(self, value: str):
        value = value.strip()
        if not re.match(r"^\+?[0-9\- ]{7,20}$", value):
            raise ValueError("Numero di telefono non valido.")
        self._dto.telefono = value

    # DTO validato
    def to_dto(self) -> Utente:
        return self._dto
    