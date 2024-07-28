from flask import Flask, request
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

app = Flask(__name__)

load_dotenv()

store = {}

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

with_message_history = RunnableWithMessageHistory(llm, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

@app.route("/")
def hello_world():
  response = with_message_history.invoke(
    [HumanMessage(content=request.args.get("message"))],
    config=config
  )
  return response.content