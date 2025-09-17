import logging
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from unidecode import unidecode

from config import MEDIA_DIR
from models import Gincana, Organizadora, Tarefa
from repository import TarefaRepository

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(
        self,
        tarefa_repository: TarefaRepository,
        gincana: Gincana,
        organizadora: Organizadora,
    ):
        self.tarefa_repository = tarefa_repository
        self.gincana = gincana
        self.organizadora = organizadora

    @abstractmethod
    def scrape_tarefas(self, limit: None | int = None) -> list[Tarefa]:
        pass

    def gen_new_pdf_path(self, tarefa: Tarefa) -> Path:
        """Gera um novo caminho para o arquivo PDF da tarefa"""
        nome_organizadora = unidecode(self.organizadora.nome).replace(" ", "_")
        nome_gincana = unidecode(self.gincana.nome).replace(" ", "_")

        nome_tarefa = unidecode(tarefa.nome).replace(" ", "_")
        nome_tarefa = f"{nome_tarefa}-{str(uuid.uuid4())[:4]}"

        directory = MEDIA_DIR / nome_organizadora / nome_gincana
        directory.mkdir(parents=True, exist_ok=True)

        return directory / f"{nome_tarefa}.pdf"

    def get_pdf_path_for_tarefa(self, tarefa: Tarefa) -> Path:
        if tarefa.id_interno is None:
            raise ValueError("Tarefa não possui ID interno")

        path = self.tarefa_repository.get_existing_pdf_path(
            tarefa.gincana_id, tarefa.id_interno
        )

        if path:
            logger.info(
                f"Arquivo PDF encontrado para tarefa {tarefa.id_interno} ({path})"
            )
            return path

        logger.info(
            f"Arquivo PDF não encontrado para tarefa {tarefa.id_interno}, buscando..."
        )
        return self.handle_pdf(tarefa)

    @abstractmethod
    def handle_pdf(self, tarefa: Tarefa) -> Path:
        pass

    @staticmethod
    @abstractmethod
    def get_nome_organizadora() -> str:
        pass
