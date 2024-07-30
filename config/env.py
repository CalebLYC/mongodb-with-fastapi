import os
from dotenv import load_dotenv


load_dotenv()

def env(variable: str):
    return os.getenv(variable)