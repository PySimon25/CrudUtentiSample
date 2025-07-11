import os
import mariadb as db
from dotenv import load_dotenv
from repository import UtenteDAOMariaDB
from service import UtenteService

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

dao = UtenteDAOMariaDB(conn)
service = UtenteService(dao)

user = service.recupera_utente(1)
print(user)

print("-------")

users = service.recupera_tutti()
print(users)
