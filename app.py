from flask import Flask, request
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

@app.route("/")
def hello_world():
  response = llm.invoke([HumanMessage(content=request.args.get("message"))])
  return response.content