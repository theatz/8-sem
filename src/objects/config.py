from pydantic import BaseSettings, Field
class MyConfig(BaseSettings):
    ELK_URL: str = Field(..., env="ELK_URL")
    ELK_USER: str = Field(..., env="ELK_USER")
    ELK_PASS: str = Field(..., env="ELK_PASS")
    RMQ_HOST: str = Field(..., env="RMQ_HOST")
    RMQ_PORT: int = Field(default=5672, env="RMQ_PORT")
    RMQ_USER: str = Field(..., env="RMQ_USER")
    RMQ_PASS: str = Field(..., env="RMQ_PASS")

config = MyConfig(_env_file=".env")