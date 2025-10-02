from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_hostname: str = Field(..., json_schema_extra={"env": "DATABASE_HOSTNAME"})
    database_port: int = Field(..., json_schema_extra={"env": "DATABASE_PORT"})
    database_password: str = Field(..., json_schema_extra={"env": "DATABASE_PASSWORD"})
    database_name: str = Field(..., json_schema_extra={"env": "DATABASE_NAME"})
    database_username: str = Field(..., json_schema_extra={"env": "DATABASE_USERNAME"})

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
