import httpx

from config import WUZAPI_SERVER_URL, WUZAPI_TOKEN
from models import Tarefa
from senders.base_sender import BaseSender


class WuzapiSender(BaseSender):
    def send_tarefa(self, tarefa: Tarefa) -> bool:
        with httpx.Client(
            base_url=WUZAPI_SERVER_URL, headers={"token": WUZAPI_TOKEN}
        ) as client:
            body = {
                "Phone": self.gincana.id_grupo_whatsapp,
                "Document": f"data:application/octet-stream;base64,{tarefa.get_base64_encoded_file_data()}",
                "FileName": f"{tarefa.unidecoded_name}.pdf",
                "Caption": f"{tarefa.nome}\nSetor: {tarefa.setor}\nLink: {tarefa.disponivel_em_url}",
            }

            client.post("/chat/send/document", json=body)
            return True
