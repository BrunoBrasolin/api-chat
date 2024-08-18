from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from app.tool import calculate_percentage

def handle_chat(input, language):
  search_tool = TavilySearchResults(max_results=2)

  tools=[calculate_percentage, search_tool]

  llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash").bind_tools(tools)

  prompt = hub.pull('brunobrasolin/dalme')

  agent = create_react_agent(llm, tools, prompt)

  
  agent_executor = AgentExecutor.from_agent_and_tools(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    max_iterations=3
                  )
  
  ai_msg = agent_executor.invoke({
    "language": language,
    "input": input
  })

  print("--------------------------------------------------------")
  print(ai_msg)
  print("--------------------------------------------------------")

  return ai_msg
