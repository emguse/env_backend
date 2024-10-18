import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).parent.parent.parent
env_file = ".env"
env_path = Path.joinpath(basedir, env_file)

load_dotenv(env_path, override=True)


class BaseConfig:
    PROJECT_NAME = os.environ.get("PROJECT_NAME")
    DB_USER_NAME = os.environ.get("DB_USER_NAME")
    DB_USER_PASS = os.environ.get("DB_USER_PASS")
    DB_HOST_NAME = os.environ.get("DB_HOST_NAME")
    DB_HOST_PORT = os.environ.get("DB_HOST_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_ECHO = bool(os.environ.get("DB_ECHO"))


# env = BaseConfig()
# print(env.DB_NAME)
