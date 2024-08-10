from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tracers import ConsoleCallbackHandler
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from app.tool import calculate_percentage

def handle_chat(messages, language):
  model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

  search = TavilySearchResults(max_results=2)
  tools=[search, calculate_percentage]

  prompt = hub.pull('brunobrasolin/maggie-bot')

  agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

  config = {"callbacks":[ConsoleCallbackHandler()]}

  ai_msg = agent_executor.invoke({
    "language": language,
    "message": messages
  })
  print("--------------------------------------------------------")
  print(ai_msg)
  print("--------------------------------------------------------")
  return ai_msg