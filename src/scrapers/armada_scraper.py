import logging
from datetime import datetime
from pathlib import Path

import httpx
import pdfkit

from config import MEDIA_DIR
from factory import register_scraper
from models import Tarefa
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


@register_scraper
class ArmadaScraper(BaseScraper):
    def scrape_tarefas(self, limit: None | int = None) -> list[Tarefa]:
        org = self.organizadora
        if not self.gincana.id or not self.gincana.id_interno:
            raise ValueError("Gincana não possui ID")

        with httpx.Client(base_url=org.url) as client:
            response = client.get(
                f"/api/gymkhanas/{self.gincana.id_interno}/tasks.json"
            )
            tarefas = []
            for tarefa in response.json():
                tarefa_object = Tarefa(
                    id_interno=tarefa["id"],
                    nome=f"{tarefa['number']} - {tarefa['title']}",
                    setor=tarefa["section"],
                    postada_em=datetime.strptime(
                        tarefa["published_at"], "%Y-%m-%d %H:%M:%S"
                    ),
                    gincana_id=self.gincana.id,
                    scraped_em=datetime.now(),
                )
                pdf_path = self.get_pdf_path_for_tarefa(tarefa_object)

                tarefa_object.caminho_arquivo = str(
                    pdf_path.relative_to(MEDIA_DIR)
                )

                tarefa_object.disponivel_em_url = f"https://armadaorganizadora.com.br/gymkhana/{self.gincana.id_interno}/task/{tarefa['id']}"

                tarefas.append(tarefa_object)

            return tarefas

    def handle_pdf(self, tarefa: Tarefa) -> Path:
        with httpx.Client(base_url=self.organizadora.url) as client:
            response = client.get(
                f"/api/gymkhanas/{self.gincana.id_interno}/tasks/{tarefa.id_interno}.json"
            )
            data = response.json()
            html_string = f"""
            <html>
                <div>{data["header"]}</div>
                <h1>{data["number"]} - {data["title"]}</h1>
                <div>{data["content"]}</div>
                <div>{data["instructions"]}</div>
            </html>
            """
            new_pdf_path = self.gen_new_pdf_path(tarefa)
            logger.info(f"Salvando tarefa {tarefa.nome} em {new_pdf_path}")
            pdfkit.from_string(html_string, new_pdf_path)
            logger.info(f"Tarefa {tarefa.nome} salva em {new_pdf_path}")
            return new_pdf_path

    @staticmethod
    def get_nome_organizadora() -> str:
        return "armada"
