import os


def _load_env_file(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


_load_env_file()


class Settings:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-in-production-secret")
    DEBUG: bool = os.environ.get("DEBUG", "true").lower() == "true"
    SITE_TITLE: str = os.environ.get("SITE_TITLE", "FinJust — юрист по финансовым вопросам")
    LAWYER_NAME: str = os.environ.get("LAWYER_NAME", "FinJust")
    LAWYER_PHONE: str = os.environ.get("LAWYER_PHONE", "+7 (999) 000-00-00")
    LAWYER_EMAIL: str = os.environ.get("LAWYER_EMAIL", "info@finjust.ru")
    LAWYER_ADDRESS: str = os.environ.get("LAWYER_ADDRESS", "г. Москва, ул. Примерная, д. 1, оф. 10")
    ADMIN_USERNAME: str = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "admin")


settings = Settings()
