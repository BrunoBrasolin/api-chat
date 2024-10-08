import os
from app.dto import ChatDto
from app.rag import handle_chat
import pvleopard

def rag_service(request):
    data = request
    dto = ChatDto(**data)

    response = handle_chat(input=dto.message, language=dto.language)

    return {"message": response['output'], "language": dto.language}

def transcript_audio(audio):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_directory, "dalme-leopard.pv")
    transcript = ""
    file_path = os.path.join(current_directory, "audio.wav")

    leopard = None
    try:
        audio.save(file_path)
        leopard = pvleopard.create(
            access_key=os.getenv('LEOPARD_API_KEY'),
            model_path=model_path
        )

        transcript, words = leopard.process_file(file_path)

        print(f"--> {transcript} <--")
        for word in words:
            print(
            "{word=\"%s\" start_sec=%.2f end_sec=%.2f confidence=%.2f}"
            % (word.word, word.start_sec, word.end_sec, word.confidence))
    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        if leopard: 
            leopard.delete()
        if os.path.exists(file_path): 
            os.remove(file_path)

    return {"message": transcript}