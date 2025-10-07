import os
import json
import logging
import requests
import pandas as pd
from typing import Optional, Dict, Union, Any
from datetime import datetime

# Import custom functions
from .db import *

TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

PROMPTS_FOLDER_PATH = './prompts/'

# Use our custom logger defined in main.py
logger = logging.getLogger("ai_engine_logger")

def get_agent_prompts(filename):
  try:
    with open(PROMPTS_FOLDER_PATH+filename+'.txt', 'r', encoding='utf-8') as file:
      return file.read()
  except FileNotFoundError:
    logger.error('Error: The file \'%s\' was not found.', filename)
  except Exception as e:
    logger.error('An error occurred: %s', e, exc_info=True)

# Send POST requests
def send_post_request(service_url: str, data: Dict, authorization: str = None):
  try:
    if authorization is not None:
      headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization
      }
    else:
      headers = {
        'Content-Type': 'application/json'
      }

    # For debugging / logging
    logger.debug('Body for sending POST request: %s\n', json.dumps(data, indent=2))

    response = requests.post(
      url = service_url, 
      headers = headers,
      json = data,
      verify = False  # Disable SSL verification (not recommended for production)
    )

    response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
      
    if response.status_code == 200:
      return {'response': response.text, 'status_code': response.status_code}
    else:
      return {'error': 'Failed to send POST request to service', 'status_code': response.status_code}
  
  except requests.exceptions.HTTPError as http_err:
    return {'error': f'HTTP error occurred: {http_err}', 'status_code': response.status_code if response else 503}

  except requests.exceptions.Timeout as timeout_err:
    return {'error': f'Request timed out: {timeout_err}', 'status_code': 408}
  
  except requests.exceptions.ConnectionError as conn_err:
    return {'error': f'Connection error occurred: {conn_err}', 'status_code': 400}
  
  except requests.exceptions.RequestException as req_err:
    return {'error': f'Request error occurred: {req_err}', 'status_code': 400}