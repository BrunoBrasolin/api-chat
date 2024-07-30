from langchain_core.messages import HumanMessage

from app.dto import ChatDto
from app.rag import config, handle_chat

def rag_service(request):
  data = request
  dto = ChatDto(**data)

  # response = model_with_tools.invoke(dto.message)
  # print("--------------------------------")
  # print(response)
  # print("--------------------------------")

  # tool_call = response.tool_calls[0]
  # tool_message = model_with_tools.invoke(tool_call["args"])

  
  # print("--------------------------------")
  # print(tool_message)
  # print("--------------------------------")

  # return response.content

  response = handle_chat(message = [HumanMessage(content=dto.message)], language = dto.language)

  print("--------------------------------")
  print(response)
  print("--------------------------------")

  return {"message": response.content, "language": dto.language}