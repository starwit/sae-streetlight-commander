from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

from visionlib.pipeline.settings import LogLevel, YamlConfigSettingsSource

class DataBaseConfig(BaseModel):
    hostname: str = "localhost"
    port: int = 5432
    username: str = "analytics"
    password: str = "analytics"
    database: str = "analytics"

class LampConfig(BaseModel):
    hostname: str = "localhost"
    threshold_yellow: int = 8
    threshold_red: int = 12
    observation_id: str = "area_name"

class LightsConfig(BaseSettings):
    log_level: LogLevel = LogLevel.INFO

    db: DataBaseConfig = DataBaseConfig()
    lamp: LampConfig = LampConfig()
    
    model_config = SettingsConfigDict(env_prefix='SAE_LIGHT_', env_nested_delimiter='__')

    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        return (init_settings, env_settings, YamlConfigSettingsSource(settings_cls), file_secret_settings)