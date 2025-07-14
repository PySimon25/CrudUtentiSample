import mariadb
from dto import Utente
from repository import UtenteDAOInterface

# Implementazione concreta del DAO
class UtenteDAOMariaDB(UtenteDAOInterface):

    def __init__(self, pool: mariadb.ConnectionPool) -> None:
        self.pool = pool

    def create(self, utente: Utente) -> int:
        """Implementa l'operazione CREATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Utenti (nome, cognome, email, telefono)
                    VALUES(?, ?, ?, ?)""",
                    (utente.nome, utente.cognome, utente.email, utente.telefono)
                )
                conn.commit()
                newid = cursor.lastrowid
                if newid is None:
                    raise RuntimeError("L'inserimento non ha restituito un ID.")
                return newid
        finally:
            conn.close()

    def get_by_id(self, id_utente: int) -> Utente | None:
        """Implementa l'operazione READ per ID"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_utente, nome, cognome, email, telefono FROM Utenti WHERE id_utente = ?", (id_utente,))
                row = cursor.fetchone()
                return Utente(**row) if row else None
        finally:
            conn.close()

    def get_all(self) -> list[Utente]:
        """Implementa l'operazione READ per Utenti"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_utente, nome, cognome, email, telefono FROM Utenti")
                rows = cursor.fetchall()
                return [Utente(**row) for row in rows]
        finally:
            conn.close()

    def find_by_email(self, email: str) -> Utente | None:
        """Implementa l'operazione READ per EMAIL"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_utente, nome, cognome, email, telefono FROM Utenti WHERE email = ?", (email,))
                row = cursor.fetchone()
                return Utente(**row) if row else None
        finally:
            conn.close()

    def update(self, utente: Utente) -> bool:
        """Implementa l'operazione UPDATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE Utenti SET nome = ?, cognome = ?, email = ?, telefono = ? WHERE id_utente = ?""",
                    (Utente.nome, Utente.cognome, Utente.email, Utente.telefono)
                )
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()

    def delete(self, id_utente: int) -> bool:
        """Implementa l'operazione DELETE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Utenti WHERE id_utente = ?", (id_utente,))
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()

