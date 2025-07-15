from dataclasses import dataclass

# Transfer Object (DTO) per Genere
@dataclass
class Genere:
    id_genere: int | None = None
    nome_genere: str | None = None
