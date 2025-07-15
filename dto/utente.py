from dataclasses import dataclass

# Transfer Object (DTO) per Utente
@dataclass
class Utente:
    id_utente: int | None = None
    nome: str | None = None
    cognome: str | None = None
    email: str | None = None
    telefono: str | None = None
