from abc import ABC, abstractmethod
from typing import List

from models import Gincana, Tarefa


class BaseSender(ABC):
    def __init__(self, gincana: Gincana):
        self.gincana = gincana

    @abstractmethod
    def send_tarefa(self, tarefa: Tarefa) -> bool:
        """Envia tarefas através desse canal, retorna status de sucesso"""
        pass

    def send_tarefas(self, tarefas: List[Tarefa]):
        for tarefa in tarefas:
            self.send_tarefa(tarefa)
