from pydantic import BaseModel, Field
from langchain.tools import tool
import requests


class CalculatePercentage(BaseModel):
    value: str = Field(description="valor em real para ser usado na porcentagem")

@tool("calculate_percentage", args_schema=CalculatePercentage)
def calculate_percentage(value: int):
  """Calcula a porcentagem de valores monetários entre Bruno e Letícia"""
  url = f"https://api.gamidas.dev.br/contas/conta?valor={value}"
  response = requests.get(url)
  return response.json()