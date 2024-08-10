from pydantic import BaseModel, Field
from langchain.tools import tool
import requests


class CalculatePercentage(BaseModel):
    value: str = Field(description="value in brazilian real to use to calculate the percentage")

@tool("calculate_percentage", args_schema=CalculatePercentage)
def calculate_percentage(value: int):
  """Calculate the percentage of a money value between Bruno and Let'icia"""
  url = f"https://api.gamidas.dev.br/contas/conta?valor={value}"
  response = requests.get(url)
  return response.json()