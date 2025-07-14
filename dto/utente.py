from dataclasses import dataclass

# Transfer Object (DTO) per Utente
@dataclass
class Utente:
    id_utente: int | None = None
    nome: str = ""
    cognome: str = ""
    email: str = ""
    telefono: str = ""
