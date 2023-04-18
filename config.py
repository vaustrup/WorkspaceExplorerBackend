from dataclasses import dataclass


@dataclass
class Config:
    TESTING = False
    SECRET_KEY = "asdsadads"

@dataclass
class DevelopmentConfig(Config):
    TESTING = True
