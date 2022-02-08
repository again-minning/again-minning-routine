from pydantic import BaseSettings
from config.constants import DeployState
from decouple import config as de_config


class DefaultSettings(BaseSettings):
    ENV_STATE: str = 'local'
    APP_ENV: str = 'local'
    DATABASE_URL: str
    SHOW_SQL: bool = False
    MONGO_URL: str

    class Config:
        env_file = '.env'


class StagingSettings(DefaultSettings):
    class Config:
        env_file = 'staging.env'


class ProductionSettings(DefaultSettings):
    class Config:
        env_file = 'production.env'


class TestSettings(DefaultSettings):
    class Config:
        env_file = 'test.env'


class FactorySettings:
    @staticmethod
    def load():
        env_state = de_config('APP_ENV', 'local')
        if env_state == DeployState.STAGING.value:
            return StagingSettings()
        elif env_state == DeployState.PRODUCTION.value:
            return ProductionSettings()
        elif env_state == DeployState.TEST.value:
            return TestSettings()
        else:
            return DefaultSettings()


settings = FactorySettings().load()
