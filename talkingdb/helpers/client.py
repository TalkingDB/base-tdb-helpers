import os
from dotenv import load_dotenv
from talkingdb.models.api.mode import ClientMode

load_dotenv()

CLIENT_MODE = os.getenv("CLIENT_MODE", ClientMode.DIRECT)
CE_HOST = os.getenv("CE_HOST", None)


class Config:
    CLIENT_MODE: ClientMode = CLIENT_MODE
    API_TIMEOUT = 300
    CE_HOST = CE_HOST


config = Config()
