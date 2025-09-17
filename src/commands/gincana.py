import datetime
import logging

import click

from db_session import get_session
from models import Gincana
from repository import GincanaRepository, OrganizadoraRepository

logger = logging.getLogger(__name__)


@click.group()
def gincana_group():
    """Comandos relacionados a ginanas."""
    pass


@gincana_group.command()
@click.argument("nome")
@click.option("--organizadora", required=True)
@click.option(
    "--inicio",
    type=click.DateTime(
        formats=[
            "%d/%m/%Y",
        ]
    ),
    help="Data de início da ginana",
    required=True,
)
@click.option(
    "--duracao", type=int, help="Duração da gincana em dias", required=True
)
@click.option("--id_interno", help="id usado pela organizadora")
def add(
    nome: str,
    organizadora: str,
    inicio: datetime.datetime,
    duracao: int,
    id_interno: str,
):
    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        if (org := organizadora_repo.find_by_nome(organizadora)) is None:
            click.echo(f"Organizadora {organizadora} não encontrada.")
            return
        if org.id is None:
            click.echo("Organizadora encontrada mas id é nulo.")
            return

        gincana_repo = GincanaRepository(session)
        gincana = Gincana(
            id_interno=id_interno,
            nome=nome,
            organizadora_id=org.id,
            inicio=inicio,
            fim=inicio + datetime.timedelta(days=duracao),
        )
        gincana_repo.add(gincana)

        click.echo(f"Gincana {nome} adicionada com sucesso.")
