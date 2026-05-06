import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    plovercast_api_key: str
    plovercast_base_url: str
    database_url: str
    tz: str


def load():
    return Settings(
        plovercast_api_key=os.environ["PLOVERCAST_API_KEY"],
        plovercast_base_url=os.environ.get("PLOVERCAST_BASE_URL") or "https://api.plovercast.com/v3",
        database_url=os.environ["PULSE_DATABASE_URL"],
        tz=os.environ.get("PULSE_TZ") or "America/Toronto",
    )
