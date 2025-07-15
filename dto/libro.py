from dataclasses import dataclass

# Transfer Object (DTO) per Libro
@dataclass
class Libro:
    id_libro: int | None = None
    id_biblioteca: int = 0
    titolo: str | None = None
    autore: str | None = None
    anno_pubblicazione: int | None = None
    isbn: str | None = None
    id_categoria: int = 0
    id_genere: int = 0
