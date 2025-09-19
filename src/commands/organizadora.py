import click
import questionary

from db_session import get_session
from models import Organizadora
from repository import OrganizadoraRepository

import logging

logger = logging.getLogger(__name__)


@click.group(name="organizadora")
def organizadora_group():
    """Comandos relacionados a organizadoras."""
    pass


@organizadora_group.command
def add():
    nome = questionary.text(message="Nome da organizadora").ask()

    available_scrapers = __import__("scrapers").__all__
    scraper_class = questionary.select(
        message="Classe do Scraper para a organizadora",
        instruction="Implementado no módulo scrapers",
        choices=available_scrapers,
    ).ask()

    url = questionary.text(
        message="URL base do site da organizadora", instruction="sem a última /"
    ).ask()

    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        if organizadora_repo.find_by_nome(nome):
            logger.fatal(f"Organizadora '{nome}' já existe.")
            return

        organizadora = Organizadora(nome=nome, scraper_class=scraper_class, url=url)
        organizadora_repo.add(organizadora)
        logger.info(f"Organizadora '{nome}' adicionada com sucesso.")


@organizadora_group.command
def list():
    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        organizadoras = organizadora_repo.list()

        if not organizadoras:
            logger.fatal("Nenhuma organizadora encontrada.")
            return

        logger.info(f"Organizadoras: {', '.join([o.nome for o in organizadoras])}")
