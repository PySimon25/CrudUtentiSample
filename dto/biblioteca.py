from dataclasses import dataclass

# Transfer Object (DTO) per Biblioteca
@dataclass
class Biblioteca:
    id_biblioteca: int | None = None
    nome_biblioteca: str | None = None
    citta: str | None = None
    indirizzo: str | None = None
