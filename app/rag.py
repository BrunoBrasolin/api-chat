from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from app.tool import calculate_percentage

def handle_chat(messages, language):
  search_tool = TavilySearchResults(max_results=2)

  tools=[calculate_percentage, search_tool]

  llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash").bind_tools(tools)

  prompt = hub.pull('brunobrasolin/delma')

  agent = create_react_agent(llm, tools, prompt)

  agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    handle_parsing_errors=True,
                    max_execution_time=30,
                    max_iterations=3
                  )
  
  ai_msg = agent_executor.invoke({
    "language": language,
    "message": messages
  })

  print("--------------------------------------------------------")
  print(ai_msg)
  print("--------------------------------------------------------")

  return ai_msg