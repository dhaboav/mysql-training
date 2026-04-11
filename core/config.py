"""General Configuration FastAPI application.

This module provides class for configuration in application.

Features:
    - Take information from .env.
    - Setup project title.
    - Configure mysql database url.
"""

from pydantic import MySQLDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for application configuration."""

    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )

    PROJECT_NAME: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
        )


settings = Settings()
