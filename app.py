from flask import Flask, request
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = Flask(__name__)

load_dotenv()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

store = {}

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

config = {"configurable": {"session_id": "abc"}}

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "Your name is MaggieBot. You are a chatbot made to help Bruno and Letícia, they are fiances. Answear all questions in {language}",
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)

chain = prompt| llm

with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

@app.route("/")
def hello_world():
  response = with_message_history.invoke(
    {
      "messages": [HumanMessage(content=request.args.get("message"))],
      "language": "english"
    },
    config=config
  )
  return response.content