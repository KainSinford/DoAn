from pydantic import BaseSettings


class Settings(BaseSettings):
    # MySQL
    MYSQL_URL: str = "mysql+pymysql://root:password@mysql:3306/webstore"

    # PostgreSQL
    POSTGRES_URL: str = "postgresql://postgres:password@postgres:5432/finance"

    # App
    APP_NAME: str = "Dashboard Service"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
