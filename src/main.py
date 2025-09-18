import logging

from commands import cli
from db_session import init_db

if __name__ == "__main__":
    logging.info("Iniciando aplicação")
    init_db()
    cli()
