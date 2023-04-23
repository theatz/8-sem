from pydantic import BaseSettings, Field
import os

class MyConfig(BaseSettings):
    ELK_URL: str = Field(..., env="ELK_URL")
    ELK_USER: str = Field(..., env="ELK_USER")
    ELK_PASS: str = Field(..., env="ELK_PASS")

print(os.system('pwd'))
config = MyConfig(_env_file=".env")