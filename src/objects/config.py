from pydantic import BaseSettings, Field
class MyConfig(BaseSettings):
    ELK_URL: str = Field()
    ELK_USER: str = Field()
    ELK_PASS: str = Field()
    RMQ_HOST: str = Field()
    RMQ_PORT: int = Field(default=5672)
    RMQ_USER: str = Field()
    RMQ_PASS: str = Field()

config = MyConfig(_env_file=".env")