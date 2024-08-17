import os
import tempfile
from app.dto import ChatDto
from app.rag import handle_chat
import pvleopard

def rag_service(request):
  data = request
  dto = ChatDto(**data)

  response = handle_chat(messages = dto.message, language = dto.language)

  return {"message": response['output'], "language": dto.language}

def transcript_audio(audio_storage):
  current_directory = os.path.dirname(os.path.abspath(__file__))
  model_path = os.path.join(current_directory, "dalme-leopard.pv")

  with tempfile.NamedTemporaryFile(delete=False, suffix=".pv") as temp_file:
    file_path = temp_file.name
    audio_storage.save(file_path)

  leopard = pvleopard.create(
    access_key=os.getenv('LEOPARD_API_KEY'),
    model_path=model_path)

  transcript, words = leopard.process_file(file_path)
  print(transcript)
  for word in words:
    print(
      "{word=\"%s\" start_sec=%.2f end_sec=%.2f confidence=%.2f}"
      % (word.word, word.start_sec, word.end_sec, word.confidence))

  leopard.delete()
  os.remove(file_path)

  response = handle_chat(messages=transcript, language="portuguese")

  return {"message": response['output'], "language": "portuguese"}