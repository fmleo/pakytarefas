import logging

import click

from commands.tarefa import tarefa_group

from .gincana import gincana_group
from .organizadora import organizadora_group

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


cli.add_command(gincana_group)
cli.add_command(organizadora_group)
cli.add_command(tarefa_group)
