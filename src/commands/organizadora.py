import click

from db_session import get_session
from models import Organizadora
from repository import OrganizadoraRepository


@click.group(name="organizadora")
def organizadora_group():
    """Comandos relacionados a organizadoras."""
    pass


@organizadora_group.command
@click.option("--nome", required=True, help="Nome da organizadora")
@click.option("--scraper_class", required=True, help="Classe do Scraper para a organizadora, implementado no módulo scrapers")
@click.option("--url", required=True, help="URL base do site da organizadora, sem a última /")
def add(nome: str, scraper_class: str, url: str):
    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        if organizadora_repo.find_by_nome(nome):
            click.echo(f"Organizadora '{nome}' já existe.")
            return

        organizadora = Organizadora(
            nome=nome, scraper_class=scraper_class, url=url
        )
        organizadora_repo.add(organizadora)
        click.echo(f"Organizadora '{nome}' adicionada com sucesso.")


@organizadora_group.command
def list():
    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        organizadoras = organizadora_repo.list()

        if not organizadoras:
            click.echo("Nenhuma organizadora encontrada.")
            return

        click.echo("Organizadoras:")
        for organizadora in organizadoras:
            click.echo(f"- {organizadora.nome}")
