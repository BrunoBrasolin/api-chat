from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent
from app.tool import calculate_percentage

def handle_chat(messages, language):
  system_prompt = '''
    Your name is MaggieBot;\n
    You are a chatbot made to help Bruno and Letícia, they are fiances;\n
    You should answer formally;\n
    You should not use emoji;\n
    You have access to the following tools: {tools};\n
    Action: the action to take, should be one of [{tool_names}];\n
    Answear all questions in {language};\n
    Begin!

    Question: {message}
    Thought:{agent_scratchpad}.\n\n
  '''

  prompt = ChatPromptTemplate.from_messages(
    [
      (
        "system",
        system_prompt
      ),
      MessagesPlaceholder(variable_name="messages")
    ]
  )

  model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

  search = TavilySearchResults(max_results=2)
  tools=[search, calculate_percentage]


  model_with_tools = model.bind_tools(tools)

  formatted_prompt = prompt.format(language=language, messages=[HumanMessage(content=messages)])

  prompt = PromptTemplate(system_prompt)

  agent_executor = create_react_agent(llm=model, tools=tools, prompt=prompt)

  ai_msg = agent_executor.invoke({
    "language": language,
    "message": messages
  })
  print("----------------------------------------------------------")
  print(ai_msg)
  print("----------------------------------------------------------")
  return ai_msg