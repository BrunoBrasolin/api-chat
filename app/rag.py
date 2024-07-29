from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

system_prompt = (
  "Your name is MaggieBot;\n"
  "You are a chatbot made to help Bruno and Letícia, they are fiances;\n"
  "You should answer formally;\n"
  "You should not use emoji;\n"
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

config = {"configurable": {"session_id": "abc"}}

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

search = TavilySearchResults(max_results=2)
search_results = search.invoke("Kanoa ou Medina venceu nas olimpiadas de 2024?")
tools=[search]

model_with_tools = model.bind_tools(tools)

chain = prompt | model_with_tools

with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")