import mariadb
from dto import Libro
from repository import LibroDAOInterface

class LibroDAOMariaDB(LibroDAOInterface):

    def __init__(self, pool: mariadb.ConnectionPool) -> None:
        self.pool = pool

    def create(self, libro: Libro) -> int:
        """Implementa l'operazione CREATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execite(
                    """INSERT INTO Libri (id_biblioteca, titolo, autore, anno_pubblicazione, isbn, id_categoria, id_genere)
                    VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (libro.id_biblioteca, libro.titolo, libro.autore, libro.anno_pubblicazione, libro.isbn, libro.id_categoria, libro.id_genere)
                )
                conn.commit()
                newid = cursor.lastrowid
                if newid is None:
                    raise RuntimeError("L'inserimento non ha restituito un ID.")
                return newid
        finally:
            conn.close()

    def get_by_id(self, id_libro: int) -> Libro | None:
        """Implementa l'operazione READ per ID"""
        raise NotImplementedError()
    
    def get_all(self) -> list[Libro]:
        """Implementa l'operazione READ per Libri"""
        raise NotImplementedError()
    
    def update(self, libro: Libro) -> bool:
        """Implementa l'operazione UPDATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE Libri SET id_biblioteca = ?, titolo = ?, autore = ?, anno_pubblicazione = ?, isbn = ?, id_categoria = ?, id_genere = ? WHERE id_libro = ?""",
                    (libro.id_biblioteca, libro.titolo, libro.autore, libro.anno_pubblicazione, libro.id_categoria, libro.id_genere, libro.id_libro)
                )
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()
    
    def delete(self, id_libro: int) -> bool:
        """Implementa l'operazione DELETE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM LIbri WHERE id_libro = ?", (id_libro,))
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()
