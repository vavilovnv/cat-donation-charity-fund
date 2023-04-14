from typing import Optional

from gunicorn.app.wsgiapp import WSGIApplication
from pydantic import BaseSettings, EmailStr


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


class Settings(BaseSettings):
    app_title: str = 'API QRKot'
    app_desc: str = 'Сервис учета пожертвований на котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'any_secret'
    project_host: str = '127.0.0.1'
    project_port: int = 8000
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
