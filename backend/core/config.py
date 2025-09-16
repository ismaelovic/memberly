from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Database settings
    database_url: str = Field(..., alias="DATABASE_URL")

    # Redis settings
    redis_url: str = Field(..., alias="REDIS_URL")

    # Application settings
    debug: bool = Field(default=True, alias="DEBUG")
    secret_key: str = Field(..., alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=1440, alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )

    # Multi-tenant settings
    default_tenant: str = Field(default="default", alias="DEFAULT_TENANT")

    # Test database settings
    # test_database_url: str = Field(..., alias="TEST_DATABASE_URL")

    model_config = {
        "env_file": ".env",
        "env_prefix": "",
    }


settings = Settings()  # type: ignore
