from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from app.tool import calculate_percentage
from operator import attrgetter

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
    MessagesPlaceholder(variable_name="message")
  ]
)

config = {"configurable": {"session_id": "abc"}}

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

search = TavilySearchResults(max_results=2)
tools=[search, calculate_percentage]

model_with_tools = model.bind_tools(tools)

def handle_chat(message, language):
  formatted_prompt = prompt.format(language=language, message=message)
  ai_msg = model_with_tools.invoke(formatted_prompt)
  selected_tool = {"calculate_percentage": calculate_percentage}[ai_msg[0]["name"].lower()]
  for tool_call in ai_msg.tool_calls:
    selected_tool = {"calculate_percentage": calculate_percentage}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    return tool_msg