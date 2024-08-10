from app.dto import ChatDto
from app.rag import handle_chat

def rag_service(request):
  data = request
  dto = ChatDto(**data)

  response = handle_chat(messages = dto.message, language = dto.language)

  return {"message": response['output'], "language": dto.language}