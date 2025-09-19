import datetime
import logging

import click
import httpx
import questionary
from typing_extensions import List

from config import WUZAPI_SERVER_URL, WUZAPI_TOKEN
from db_session import get_session
from models import Gincana
from repository import GincanaRepository, OrganizadoraRepository

logger = logging.getLogger(__name__)


@click.group()
def gincana_group():
    """Comandos relacionados a ginanas."""
    pass


@gincana_group.command()
def add():
    with get_session() as session:
        organizadora_repo = OrganizadoraRepository(session)

        nome = questionary.text(message="Nome da gincana").ask()

        organizadoras = [o.nome for o in organizadora_repo.list()]
        organizadora = questionary.select(
            message="Organizadora", choices=organizadoras
        ).ask()

        inicio_str = questionary.text(
            message="Data de início da gincana", instruction="dd/mm/aaaa"
        ).ask()
        inicio = datetime.datetime.strptime(inicio_str, "%d/%m/%Y")

        fim_str = questionary.text(
            "Data de fim da gincana", instruction="dd/mm/aaaa"
        ).ask()
        fim = datetime.datetime.strptime(fim_str, "%d/%m/%Y")
        fim += datetime.timedelta(hours=23, minutes=59)

        id_interno = questionary.text(message="ID Usado pela organizadora").ask()

        grupos_whatsapp: List[questionary.Choice] = []
        with httpx.Client(
            base_url=WUZAPI_SERVER_URL, headers={"token": WUZAPI_TOKEN}
        ) as client:
            response = client.get("/group/list")
            body = response.json()["data"]
            for group in body["Groups"]:
                grupos_whatsapp.append(
                    questionary.Choice(title=group["Name"], value=group["JID"])
                )

        id_grupo_whatsapp = questionary.select(
            message="Grupo no qual enviar tarefas", choices=grupos_whatsapp
        ).ask()

        if (org := organizadora_repo.find_by_nome(organizadora)) is None:
            logger.fatal(f"Organizadora {organizadora} não encontrada.")
            return
        if org.id is None:
            logger.fatal("Organizadora encontrada mas id é nulo.")
            return

        gincana_repo = GincanaRepository(session)
        gincana = Gincana(
            id_interno=id_interno,
            nome=nome,
            organizadora_id=org.id,
            inicio=inicio,
            fim=fim,
            id_grupo_whatsapp=id_grupo_whatsapp,
        )
        gincana_repo.add(gincana)

        logger.info(f"Gincana {nome} adicionada com sucesso.")
