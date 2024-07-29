from flask import Flask, request
from dotenv import load_dotenv

from app.service import rag_service

app = Flask(__name__)

load_dotenv("/app/config/.env")

@app.route("/", methods=["POST"])
def chat():
  result = rag_service(request.get_json())
  return result

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
  return {"status": "Healthy"}