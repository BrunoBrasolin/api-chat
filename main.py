from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

from app.service import rag_service, transcript_audio

app = Flask(__name__)
cors = CORS(app)

load_dotenv("/app/config/.env")

@app.route("/message", methods=["POST"])
@cross_origin()
def message():
  result = rag_service(request.get_json())
  return result

@app.route("/transcript_audio", methods=["POST"])
@cross_origin()
def audio():
  audio = request.files['audio']
  result = transcript_audio(audio)
  return result

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
  return {"status": "Healthy"}