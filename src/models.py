import base64
import datetime
from typing import List, Optional

import unidecode
from sqlmodel import Field, Relationship, SQLModel

from config import MEDIA_DIR


class Organizadora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scraper_class: str
    nome: str
    url: str

    gincanas: List["Gincana"] = Relationship(back_populates="organizadora")


class Gincana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    inicio: datetime.date
    fim: datetime.date

    organizadora_id: int = Field(foreign_key="organizadora.id")
    organizadora: Organizadora = Relationship(back_populates="gincanas")

    tarefas: List["Tarefa"] = Relationship(back_populates="gincana")

    id_interno: Optional[str]

    id_grupo_whatsapp: Optional[str] = Field()


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    caminho_arquivo: Optional[str] = Field(default=None)
    setor: Optional[str]
    postada_em: datetime.datetime
    scraped_em: datetime.datetime

    gincana_id: int = Field(foreign_key="gincana.id")
    gincana: Gincana = Relationship(back_populates="tarefas")

    id_interno: Optional[str]

    disponivel_em_url: Optional[str] = Field(default=None)

    @property
    def unidecoded_name(self) -> str:
        return unidecode.unidecode(self.nome).replace(" ", "_")

    def get_base64_encoded_file_data(self) -> Optional[str]:
        if self.caminho_arquivo:
            with open(MEDIA_DIR / self.caminho_arquivo, "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        return None
