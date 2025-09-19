from dotenv import load_dotenv
from pydantic import BaseModel
import os
load_dotenv()

class Configuration(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI", "")

