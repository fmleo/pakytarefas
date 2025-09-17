import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


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
