from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    SECRET_KEY: str
    ENVIRONMENT: str
    DEBUG: bool
    VERSION: str
    ALGORITHM: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    @property
    def db_url(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
settings = Settings()