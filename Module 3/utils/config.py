from pydantic import BaseSettings


class Settings(BaseSettings):
    # MySQL
    MYSQL_URL: str = "mysql+pymysql://root:root@mysql:3306/noah"

    # PostgreSQL
    POSTGRES_URL: str = "postgresql://postgres:root@postgres:5432/noah"

    # App
    APP_NAME: str = "Dashboard Service"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
