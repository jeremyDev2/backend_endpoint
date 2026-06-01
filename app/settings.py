from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, AmqpDsn


class Settings(BaseSettings):

    redis_dns: RedisDsn
    pg_dns: PostgresDsn
    amqp_dns: AmqpDsn

    class Config():
        env_file = ".env"

settings = Settings()
