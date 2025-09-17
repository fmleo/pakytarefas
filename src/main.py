import logging

from commands import cli
from db_session import init_db

if __name__ == "__main__":
    logging.info("Iniciando aplicação")
    init_db()
    cli()

    # with get_session() as session:
    #     gincana_repo = GincanaRepository(session)

    #     for g in gincana_repo.get_active_gincanas():
    #         print(g)

    # print(ScraperFactory.get_all_scrapers())
