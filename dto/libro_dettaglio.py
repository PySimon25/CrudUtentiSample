from dataclasses import dataclass

# Questo DTO viene utilizzato solo per restituire dati del libro
class LibroDettaglio:
    id_libro: int | None = None
    biblioteca: str = ""
    titolo: str | None = None
    autore: str | None = None
    anno_pubblicazione: int | None = None
    isbn: str | None = None
    categoria: int = 0
    genere: int = 0