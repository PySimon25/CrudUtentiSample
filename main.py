import os
import mariadb as db
from dotenv import load_dotenv
from repository import LibroDAOMariaDB, UtenteDAOMariaDB, PrestitoDAOMariaDB
from service import PrestitoService, UtenteService

load_dotenv()

conn = db.ConnectionPool(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=3306,
    database=os.getenv("DB_NAME"),
    pool_name="default_pool",
    pool_size=5
)

utente_dao = UtenteDAOMariaDB(conn)
utente_service = UtenteService(utente_dao)

user = utente_service.recupera_utente(1)
print(user)
print("-------")

#users = utente_service.recupera_tutti()
#print(users)
#print("-------")

try:
    result = utente_service.registra_utente("Ennio", "Passalacqua", "stefanibonanno@pozzecco-morpurgo.com", "+39 522 482511")
    print(result)
except Exception as ex:
    print(ex)

print("-------")

prestito_dao = PrestitoDAOMariaDB(conn)
prestito_service = PrestitoService(prestito_dao)

p1 = prestito_service.recupera_prestito(1)
print(p1)
print("-------")

p2 = prestito_service.recupera_prestiti_utente(8)
for row in p2:
    print(p2)
    print("-------")

#libro_dao = LibroDAOMariaDB(conn)
