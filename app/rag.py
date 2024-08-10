from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from app.tool import calculate_percentage

def handle_chat(messages, language):
  llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

  tools=[calculate_percentage]

  prompt = hub.pull('brunobrasolin/maggie-bot')

  agent = create_react_agent(llm, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

  ai_msg = agent_executor.invoke({
    "language": language,
    "message": messages
  })

  print("--------------------------------------------------------")
  print(ai_msg)
  print("--------------------------------------------------------")

  return ai_msg