from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tracers import ConsoleCallbackHandler
from langchain.agents import create_react_agent, AgentExecutor
from app.tool import calculate_percentage

def handle_chat(messages, language):
  system_prompt = '''
    Your name is MaggieBot
    You are a chatbot made to help Bruno and Letícia, they are fiances
    You should answer formally
    You should not use emoji
    You have access to the following tools: {tools}
    Answear all questions in {language}
    Begin!

    Question: {message}
    Action: the action to take, should be one of [{tool_names}] or no tools, just answer the question with previus knowledge
    Thought: {agent_scratchpad}
    Action Input: select one tool or just answer the question
  '''
  model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

  search = TavilySearchResults(max_results=2)
  tools=[search, calculate_percentage]

  prompt = PromptTemplate(template=system_prompt)

  agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

  config = {"callbacks":[ConsoleCallbackHandler()]}

  ai_msg = agent_executor.invoke({
    "language": language,
    "message": messages
  })
  print("--------------------------------------------------------")
  print(ai_msg['output'])
  print("--------------------------------------------------------")
  return ai_msg