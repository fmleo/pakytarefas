import logging
from datetime import datetime
from operator import and_
from pathlib import Path
from typing import Generic, Optional, Sequence, Type, TypeVar

from sqlmodel import Session, SQLModel, select
from typing_extensions import List

from config import MEDIA_DIR
from models import Gincana, Organizadora, Tarefa

T = TypeVar("T", bound=SQLModel)

logger = logging.getLogger(__name__)


class Repository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def add_all(self, objs: List[T]) -> List[T]:
        self.session.add_all(objs)
        self.session.commit()
        return objs

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def list(self) -> Sequence[T]:
        return self.session.exec(select(self.model)).all()

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()


class OrganizadoraRepository(Repository[Organizadora]):
    def __init__(self, session: Session):
        super().__init__(Organizadora, session)

    def find_by_nome(self, nome: str) -> Organizadora | None:
        return self.session.exec(
            select(Organizadora).where(Organizadora.nome == nome)
        ).first()


class GincanaRepository(Repository[Gincana]):
    def __init__(self, session: Session):
        super().__init__(Gincana, session)

    def get_active_gincanas(self) -> Sequence[Gincana]:
        return self.session.exec(
            select(Gincana).where(
                and_(
                    Gincana.inicio <= datetime.now(),
                    Gincana.fim >= datetime.now(),
                )
            )
        ).all()


class TarefaRepository(Repository[Tarefa]):
    def __init__(self, session: Session):
        super().__init__(Tarefa, session)

    def _exists_by_id_interno(self, id_interno: Optional[str]) -> bool:
        if not id_interno:
            return False

        return (
            self.session.exec(
                select(Tarefa).where(Tarefa.id_interno == id_interno)
            ).first()
            is not None
        )

    def save_new_tarefas_for_gincana(
        self, gincana_id: int, tarefas: List[Tarefa]
    ) -> List[Tarefa]:
        new_tarefas = []
        for tarefa in tarefas:
            if not self._exists_by_id_interno(tarefa.id_interno):
                logger.info(
                    f"Salvando nova tarefa com id interno {tarefa.id_interno}"
                )
                self.add(tarefa)
                new_tarefas.append(tarefa)

        return new_tarefas

    def get_existing_pdf_path(
        self, gincana_id: int, id_interno: str
    ) -> Optional[Path]:
        existing = self.session.exec(
            select(Tarefa).where(
                Tarefa.gincana_id == gincana_id, Tarefa.id_interno == id_interno
            )
        ).first()

        if (
            existing
            and existing.caminho_arquivo
            and Path(MEDIA_DIR / existing.caminho_arquivo).exists()
        ):
            return Path(MEDIA_DIR / existing.caminho_arquivo)
        else:
            return None
