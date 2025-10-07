import os
import re
import json
import logging
import requests
from typing import Optional, Dict, Union, Any, List
from typing_extensions import TypedDict

# Third party packages
import tavily
import certifi
import yfinance as yf
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Import langchain
from langchain.docstore.document import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import Graph, StateGraph, END

# Import custom functions
from .utils import (
 get_agent_prompts
)

# Use our custom logger defined in main.py
logger = logging.getLogger("ai_engine_logger")

logger.debug('Certificate: %s', certifi.where())

# Exports secret credentials from .env
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
MONGODB_ATLAS_CLUSTER_URI = os.environ.get('MONGODB_ATLAS_CLUSTER_URI')
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')
MONGODB_COLLECTION_NAME = os.environ.get('MONGODB_COLLECTION_NAME')
MONGODB_ATLAS_VECTOR_SEARCH_INDEX_NAME = os.environ.get('MONGODB_ATLAS_VECTOR_SEARCH_INDEX_NAME')

os.environ["SSL_CERT_FILE"] = certifi.where()

# Initialize MongoDB python client
mongo_client = MongoClient(MONGODB_ATLAS_CLUSTER_URI, server_api=ServerApi('1'))
MONGODB_COLLECTION = mongo_client.get_database(MONGODB_DB_NAME).get_collection(MONGODB_COLLECTION_NAME)

# Send a ping to confirm a successful connection
try:
  mongo_client.admin.command('ping')
  logger.debug('Pinged your deployment. You successfully connected to MongoDB!')
except Exception as e:
  logger.error('Error occurred: %s', e, exc_info=True)
  raise Exception('Unable to connect to MongoDB Atlas for retrieving embeddings')

class GraphState(TypedDict):
  """
  Graph state is a dictionary that contains information we want to propagate to, and modify in, each graph node.
  """
  question: str  # User question
  generation: str  # LLM generation
  use_stock_price_fetcher: str  # 'Yes' or 'No'
  use_rag_retriever: str  # 'Yes' or 'No'
  use_web_search: str  # 'Yes' or 'No'
  stock_symbols: List[str]  # List of stock symbols to fetch
  stock_prices: Dict[str, float]  # Stock prices fetched
  max_retries: int  # Max number of retries for answer generation
  loop_step: int  # Loop counter
  documents: List[Document]  # List of retrieved documents
  retriever: Optional[Any]
  llm: Optional[Any]

def get_ticker_from_company_name(company_name):
  try:
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "India"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    company_code = data['quotes'][0]['symbol']
    return company_code
  except:
    return None

def fetch_stock_price(symbol: str) -> Optional[float]:
  """Fetches the current stock price for the given symbol."""
  ticker = yf.Ticker(symbol)
  data = ticker.history(period='1d')
  if not data.empty:
    price = data['Close'].iloc[0]
    # logger.debug('Price of %s is: %s', symbol, price)
    return price
  else:
    return None

def fetch_stock_prices(state: GraphState) -> GraphState:
  """
  Fetches stock prices for the symbols in the state.
  """
  logger.debug('---FETCH STOCK PRICES---')
  stock_symbols = state.get("stock_symbols", [])
  stock_prices = {}

  for symbol in stock_symbols:
    price = fetch_stock_price(symbol)
    if price is not None:
      stock_prices[symbol] = price
    else:
      logger.debug('Could not fetch price for symbol: %s', symbol)

  # Update state with stock prices
  state["stock_prices"] = stock_prices
  return state

def web_search(state: GraphState, web_search_tool: TavilySearchResults) -> GraphState:
  """
  Performs a web search using Tavily based on the question.
  """
  print("---WEB SEARCH (UPDATED FUNCTION)---")
  question = state["question"]
  documents = state.get("documents", [])

  # Perform the web search using TavilySearchResults
  search_results = web_search_tool.run(question)
  search_results = search_results[:3]  # Limit to top 3 results only

  # Debug: Print the search results
  logger.debug('Search results: %s', search_results)

  # Check if search_results is empty
  if not search_results:
    logger.debug('No results found.')
    state["documents"] = documents
    return state

  # Convert the results to Document objects
  for result in search_results:
    logger.debug('Result: %s', result)  # Debug print
    if isinstance(result, dict):
      # Initialize snippet as empty
      snippet = ''
      # Try to extract content from possible keys
      for key in ['snippet', 'summary', 'text', 'content', 'url', 'title', 'description']:
        value = result.get(key)
        if value and isinstance(value, str):
          snippet += f"{key.capitalize()}: {value}\n"
      if snippet:
        logger.debug('Snippet: %s', snippet)  # Debug print
        documents.append(Document(page_content=snippet))
      else:
        logger.debug('No suitable content found in result: %s', result)
    elif isinstance(result, str):
      # If the result is a string, use it directly
      logger.debug('Snippet (from string result): %s', result)  # Debug print
      documents.append(Document(page_content=result))
    else:
      logger.debug('Unexpected result format: %s', result)

  # Update the state with the new documents
  state["documents"] = documents

  # Return the updated state
  return state

def web_search_wrapper(state: GraphState):
  """Wrapper function to handle web_search with StateGraph"""
  
  web_search_tool = TavilySearchResults(k=3)  # Create the tool inside the wrapper
  return web_search(state, web_search_tool)

def retrieve_documents(state: GraphState) -> GraphState:
  """
  Retrieves documents from the vector store based on the question.
  """
  logger.debug('---RETRIEVE DOCUMENTS---')
  question = state["question"]
  retriever = state["retriever"]
  documents = retriever.get_relevant_documents(question)
  logger.info('documents: %s', documents)
  state["documents"] = documents  # Update the state with retrieved documents
  return state

def decide_next_after_master(state: GraphState) -> str:
  if state["use_stock_price_fetcher"] == "Yes":
    return "fetch_stock_prices"
  elif state["use_rag_retriever"] == "Yes":
    return "retrieve_documents"
  elif state["use_web_search"] == "Yes":
    return "web_search"
  else:
    return "generate_answer"

def decide_next_after_web_search(state: GraphState) -> str:
  """
  Decides the next node after performing web search.
  """
  # For simplicity, we proceed to generate_answer
  return "generate_answer"

def decide_next_after_stock_fetch(state: GraphState) -> str:
  """
  Decides the next node after fetching stock prices.
  """
  if state["use_rag_retriever"] == "Yes":
    return "retrieve_documents"
  elif state["use_web_search"] == "Yes":
    return "web_search"
  else:
    return "generate_answer"

def decide_next_after_retrieval(state: GraphState) -> str:
  """
  Decides the next node after retrieving documents.
  """
  if state["use_web_search"] == "Yes":
    return "web_search"
  else:
    return "generate_answer"

def master_node(state: GraphState) -> GraphState:
  """Analyzes the question and decides which tools to use, including ticker lookup."""
  logger.debug('---MASTER NODE---')
  question = state["question"]

  routing_prompt = get_agent_prompts('routing')

  try:
    logger.debug('Trying with Groq API ...')

    response = state["llm"].invoke([
      SystemMessage(content=routing_prompt),
      HumanMessage(content=f"Question: {question}")
    ])

  # Catch exceptions here
  except Exception as e:
    logger.warning('Groq initialization failed: %s. Falling back to Google Generative API.', e, exc_info=True)
    logger.debug('Now, trying with Google Generative API ...')

    # Initialize Gemini and retry ONLY FOR MASTER NODE if Groq fails
    llm = ChatGoogleGenerativeAI( #<--- Initialize the Gemini LLM here
      model='gemini-1.5-pro',
      temperature=0,
      max_tokens=None,
      timeout=29,
      max_retries=2,
      google_api_key=GEMINI_API_KEY
    )

    state["llm"] = llm  # Update the state with the new LLM

    # Retry the master_node call with Gemini
    response = state["llm"].invoke([
      SystemMessage(content=routing_prompt),
      HumanMessage(content=f"Question: {question}")
    ])

  # Added logging line
  logger.debug('Raw LLM response: %s', response.content)

  # Extract JSON using Regex
  try:
    json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
    if json_match:
      json_string = json_match.group(0)

      # Attempt to parse JSON (handle potential errors)
      try:
        decision = json.loads(json_string)
      except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}. Raw: {json_string}")
        decision = {} # Initialize as empty dict
    else:
      logger.error("No JSON found in LLM response.")
      decision = {}
  
  # Catch any other potential errors
  except Exception as e:
    logger.error(f"Unexpected error during JSON extraction: {e}")
    # Fallback to default
    decision = {}

  # Set Default Values if Keys are Missing
  decision.setdefault("use_stock_price_fetcher", "No")
  decision.setdefault("use_rag_retriever", "No")
  decision.setdefault("use_web_search", "No")
  decision.setdefault("company_names", [])

  # Extract company names for ticker lookup
  company_names = decision.get("company_names", [])
  # Check if company names were provided
  if company_names:
    stock_symbols = []
    for company_name in company_names:
      ticker = get_ticker_from_company_name(company_name)
      if ticker:
        stock_symbols.append(ticker)
        logger.debug('Found ticker symbol %s for company %s', ticker, company_name)
      else:
        logger.debug('Could not find ticker symbol for company %s', company_name)
    decision["stock_symbols"] = stock_symbols  # Update decision with ticker symbols

  state["use_stock_price_fetcher"] = decision.get("use_stock_price_fetcher", "No")
  state["use_rag_retriever"] = decision.get("use_rag_retriever", "No")
  state["use_web_search"] = decision.get("use_web_search", "No")
  state["stock_symbols"] = decision.get("stock_symbols", [])

  return state

def generate_response(query: str) -> str:
  # Tavily client
  # For Debugging / Logging               
  # logger.debug('Tavily client directory: %s', dir(tavily))

  # LLM Initialization with Groq as primary 
  # and Google Gemini as fallback 
  # Deepseek: deepseek-r1-distill-llama-70b
  # Llama: llama3-70b-8192
  llm = ChatGroq(
    model='llama3-70b-8192',
    temperature=0,
    max_tokens=None,
    timeout=29,
    max_retries=1,
    groq_api_key=GROQ_API_KEY
  )
  
  mongodb_vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
    index_name=MONGODB_ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn='cosine',
  )

  # Use the globally defined MongoDBAtlasVectorSearch
  retriever = mongodb_vector_store.as_retriever(k=3)

  graph = Graph()

  # Initialize the state
  state = GraphState(
    question=query,
    generation="",
    use_stock_price_fetcher="No",
    use_rag_retriever="No",
    use_web_search="No",
    stock_symbols=[],
    stock_prices={},
    max_retries=3,
    loop_step=0,
    documents=[],
    retriever=retriever,
    llm=llm
  )

  # Assuming GraphState and all node functions are already defined
  workflow = StateGraph(GraphState)

  # Define the nodes
  workflow.add_node("master_node", master_node)
  workflow.add_node("fetch_stock_prices", fetch_stock_prices)
  workflow.add_node("retrieve_documents", retrieve_documents)
  workflow.add_node("web_search", web_search_wrapper)  # web_search_wrapper is crucial here
  workflow.add_node("generate_answer", generate_answer)

  # Build the graph
  workflow.set_entry_point("master_node")

  workflow.add_conditional_edges(
    "master_node",
    decide_next_after_master,
    {
      "fetch_stock_prices": "fetch_stock_prices",
      "retrieve_documents": "retrieve_documents",
      "web_search": "web_search",
      "generate_answer": "generate_answer"
    },
  )

  workflow.add_conditional_edges(
    "fetch_stock_prices",
    decide_next_after_stock_fetch,
    {
      "retrieve_documents": "retrieve_documents",
      "web_search": "web_search",
      "generate_answer": "generate_answer"
    },
  )

  workflow.add_conditional_edges(
    "retrieve_documents",
    decide_next_after_retrieval,
    {
      "web_search": "web_search",
      "generate_answer": "generate_answer",
    },
  )

  workflow.add_conditional_edges(
    "web_search",
    decide_next_after_web_search,
    {
      "generate_answer": "generate_answer",
    },
  )

  # Set the finish point
  workflow.set_finish_point("generate_answer")

  # Compile the workflow
  graph = workflow.compile()

  # Run the workflow using the graph's invoke method
  final_state = graph.invoke(state)

  # Return the final generated answer
  answer = final_state["generation"]

  # For Debugging / Logging
  logger.debug('User Query: %s', query)
  logger.debug('Bot Response: %s\n', answer)

  return {"response": answer}

def generate_answer(state: GraphState) -> GraphState:
  """Generates the final answer using the collected information."""
  
  logger.debug('---GENERATE ANSWER---')
  question = state["question"]
  documents = state.get("documents", [])
  stock_prices = state.get("stock_prices", {})

  context = ""
  if stock_prices:
    stock_info = "\n".join([f"The current price of {symbol} is {price}." for symbol, price in stock_prices.items()])
    context += stock_info + "\n"
  if documents:
    docs_text = "\n".join([doc.page_content for doc in documents])
    context += docs_text

  answer_prompt = get_agent_prompts('basic-answer')
  if not context:
    context = "Answer the following question:\n" + question  #Provide default when context is empty
  
  response = state.get("llm").invoke([
    HumanMessage(content=answer_prompt),
    HumanMessage(content=context)  # Include context for better answer generation
  ])

  state["generation"] = response.content.strip()
  return state