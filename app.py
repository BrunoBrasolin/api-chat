from flask import Flask, request
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = Flask(__name__)

load_dotenv("/app/config/.env")

class ChatDto:
  def __init__(self, **kwargs) -> None:
    self.message = kwargs.get("message")
    self.language = kwargs.get("language")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

store = {}

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

config = {"configurable": {"session_id": "abc"}}

system_prompt = (
  "Your name is MaggieBot;\n"
  "You are a chatbot made to help Bruno and Letícia, they are fiances;\n"
  "You answer objectively;\n"
  "Do not use emojis on the answer;\n"
  "Answear all questions in {language}"
)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      system_prompt
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)

chain = prompt| llm

with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

@app.route("/", methods=["POST"])
def chat():
  data = request.get_json()
  dto = ChatDto(**data)

  response = with_message_history.invoke(
    {
      "messages": [HumanMessage(content=dto.message)],
      "language": dto.language
    },
    config=config
  )
  return {"message": response.content, "language": dto.language}