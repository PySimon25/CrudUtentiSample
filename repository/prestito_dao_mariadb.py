import mariadb
from dto import Prestito, PrestitoDettaglio
from repository import PrestitoDAOInterface
from datetime import date

# Implementazione concreta del DAO
class PrestitoDAOMariaDB(PrestitoDAOInterface):

    def __init__(self, pool: mariadb.ConnectionPool) -> None:
        self.pool = pool

    def assegna_prestito(self, id_utente: int, id_libro: int, id_biblioteca: int, id_bibliotecario: int, data_prevista: date) -> int:
        """Implementa l'operazione CREATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Prestiti (id_utente, id_libro, id_biblioteca, id_bibliotecario, data_prestito, data_restituzione_prevista)
                    VALUES(?, ?, ?, ?, ?, ?)""",
                    (id_utente, id_libro, id_biblioteca, id_bibliotecario)
                )
                conn.commit()
                newid = cursor.lastrowid
                if newid is None:
                    raise RuntimeError("L'inserimento non ha restituito un ID.")
                return newid
        finally:
            conn.close()  

    def get_by_id(self, id_prestito: int) -> Prestito | None:
        """Implementa l'operazione READ per ID PRESTITO"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT id_prestito, id_biblioteca, id_utente, id_libro, data_prestito, data_restituzione_prevista, 
                               data_restituzione_effettiva FROM Prestiti WHERE id_prestito = ?""", (id_prestito,))
                row = cursor.fetchone()
                return Prestito(**row) if row else None
        finally:
            conn.close()
    
    def get_dettaglio_by_id(self, id_prestito: int) -> PrestitoDettaglio | None:
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT pr.id_prestito, pr.data_prestito, pr.data_restituzione_prevista, pr.data_restituzione_effettiva, 
                               ut.nome nome_utente, ut.cognome cognome_utente, li.titolo, li.autore, li.isbn, bb.nome_biblioteca, 
                               bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               WHERE id_prestito = ?""", (id_prestito,))
                row = cursor.fetchone()
                return PrestitoDettaglio(**row) if row else None
        finally:
            conn.close()

    def get_by_id_utente(self, id_utente: int) -> list[Prestito]:
        """Implementa l'operazione READ per ID UTENTE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT id_prestito, id_biblioteca, id_utente, id_libro, data_prestito, data_restituzione_prevista, 
                               data_restituzione_effettiva FROM Prestiti WHERE id_utente = ?""", (id_utente,))
                rows = cursor.fetchall()
                return [Prestito(**row) for row in rows]
        finally:
            conn.close()

    def get_dettagli_by_id_utente(self, id_utente: int) -> list['PrestitoDettaglio']:
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT pr.id_prestito, pr.data_prestito, pr.data_restituzione_prevista, pr.data_restituzione_effettiva, 
                               ut.nome nome_utente, ut.cognome cognome_utente, li.titolo, li.autore, li.isbn, bb.nome_biblioteca, 
                               bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               WHERE pr.id_utente = ?""", (id_utente,))
                rows = cursor.fetchall()
                return [PrestitoDettaglio(**row) for row in rows]
        finally:
            conn.close()