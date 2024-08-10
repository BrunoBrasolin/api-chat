from pydantic import BaseModel, Field
from langchain.tools import tool
import requests

class CalculatePercentage(BaseModel):
    value: str = Field(description="The total amount for which the percentages need to be calculated. This value should be provided as a string representing a decimal number (e.g., '20.00'). The tool will calculate how much each individual, Bruno and Letícia, should pay based on this total amount.")

@tool("calculate_percentage", args_schema=CalculatePercentage)
def calculate_percentage(value: str) -> dict[str, float]:
  """
  Tool Description:

  This tool is an API that calculates the proportional division of a total amount between two individuals, Bruno and Letícia. The tool receives a total amount as input and returns a JSON object specifying how much each person should pay. The `Leticia` field indicates the amount Letícia owes, while the `Bruno` field indicates the amount Bruno owes. The values are expressed in decimal format and represent the proportional shares each should pay of the total amount.

  Example Usage:

  - Input: A total amount (e.g., 20.00)
  - Output: A JSON object like {'Leticia': '4.62', 'Bruno': '15.38'}, indicating that Letícia should pay R$4.62 and Bruno R$15.38 of the total amount.
  """
  try:
    response = requests.get(f"https://api.gamidas.dev.br/contas/conta?valor={value}")
    response.raise_for_status()

    return response.json()
    
  except requests.exceptions.RequestException as e:
      raise RuntimeError(f"Failed to fetch the percentage calculation. {e}")

  except ValueError as e:
      raise RuntimeError(f"Failed to parse the response data: {e}.")
