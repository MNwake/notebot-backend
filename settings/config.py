import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    MONGO_DB = os.getenv("MONGO_DB", "notebot")
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASS", "password")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
