from dataclasses import dataclass
from environs import Env


env = Env()
env.read_env()


@dataclass
class Config:
    private_key_path = env("PRIVATE_KEY_PATH")
    public_key_path = env("PUBLIC_KEY_PATH")
    algorithm = env("ALGORITHM")


def read_private_key():
    with open(config.private_key_path, "r") as private_key_file:
        return private_key_file.read()


def read_public_key():
    with open(config.public_key_path, "r") as public_key_file:
        return public_key_file.read()


config = Config()
