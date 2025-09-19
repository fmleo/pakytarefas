import logging
from typing import Type

import click

from db_session import get_session
from repository import GincanaRepository, TarefaRepository
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


@click.group()
def tarefa_group():
    """Comandos relacionados a tarefas."""
    pass


@tarefa_group.command()
def discover():
    with get_session() as session:
        gincana_repository = GincanaRepository(session)

        gincanas_ativas = gincana_repository.get_active_gincanas()

        logger.info(
            f"Foram encontradas {len(gincanas_ativas)} gincanas ativas: {', '.join([g.nome for g in gincanas_ativas])}"
        )

        for gincana in gincanas_ativas:
            if gincana.id is None:
                return

            module = __import__("scrapers")
            try:
                ScraperClass: Type[BaseScraper] = getattr(
                    module, gincana.organizadora.scraper_class
                )
            except AttributeError:
                logger.error(
                    f"Scraper da classe '{gincana.organizadora.scraper_class}' não existe."
                )
                return

            with get_session() as session:
                tarefa_repository = TarefaRepository(session)

                scraper = ScraperClass(
                    gincana=gincana,
                    tarefa_repository=tarefa_repository,
                    organizadora=gincana.organizadora,
                )

                scraped_tarefas = scraper.scrape_tarefas()

                new_tarefas = tarefa_repository.save_new_tarefas_for_gincana(
                    gincana.id, scraped_tarefas
                )

                if not new_tarefas:
                    logger.info("Nenhuma nova tarefa adicionada, finalizando...")
                    return

                for tarefa in new_tarefas:
                    ...
