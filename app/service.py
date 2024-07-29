from langchain_core.messages import HumanMessage

from app.dto import ChatDto
from app.rag import config, with_message_history

def rag_service(request):
  data = request
  dto = ChatDto(**data)

  response = with_message_history.invoke(
    {
      "messages": [HumanMessage(content=dto.message)],
      "language": dto.language
    },
    config=config
  )
  return {"message": response.content, "language": dto.language}