import os
import json
import uuid
import requests
from typing import List, Dict
import pytz
from datetime import datetime, timedelta
from typing_extensions import Annotated, TypedDict

# Import Django settings
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

# For retriving / updating DB
from chatbot.models import UserInfoRecords, UserChatRecords
from chatbot.serializers import UserInfoRecordsSerializer, UserChatRecordsSerializer

# Define Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')

AI_ENGINE_URL = os.environ.get('AI_ENGINE_URL')

# Validating input data
def validate_query_request(input_query, user_args, authenticated_user):
  # Initialize validation flag as false
  validate = 'false'
  
  if user_args.get('username', '') == authenticated_user:
    # Pass the validation flag, if everything is okay
    validate = 'true'

  # Create new request payload
  request_payload = {
    "prompt": input_query,
    "user_params": user_args,
    "validate": validate
  }

  return request_payload

def save_messages(user_id, message_request_platform, message_request_id, message, sources, feedback):
  try:
    # Ensure all the parameters are provided for saving chat history
    if not (user_id and message_request_platform and message_request_id and message):
      return JsonResponse({'error': 'insufficient parameters supplied for saving chat history'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
    
    chat_message_create_data = {
      'user_id': user_id,
      'message_request_platform': message_request_platform,
      'message_request_id': message_request_id,
      'message': message,
      'sources': sources,
      'feedback': feedback
    }

    chat_message_create_serializer = UserChatRecordsSerializer(data=chat_message_create_data)
      
    if chat_message_create_serializer.is_valid():
      chat_message_create_serializer.save()
      return JsonResponse(chat_message_create_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return JsonResponse({'error': 'record cannot be created', 'logs': chat_message_create_serializer.errors}, status=status.HTTP_400_BAD_REQUEST, safe=False)
  except Exception as e:
    return JsonResponse({'error': 'some error occured while saving user\'s last chat history to DB', 'logs': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
  
def get_answer(user_id, message):
  json_body = {
    'user': {
      'id': user_id
    },
    'conversation': {
      'platform': 'web',
      'id': str(uuid.uuid4()),
      'message': message,
      'timestamp': datetime.now(kolkata_tz).strftime('%Y:%m:%d %H:%M:%S')
    }
  }

  response = send_post_request(f'{AI_ENGINE_URL}/api/messages/', data=json_body)

  return response

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
    # print('Body for sending POST request: ', json.dumps(data, indent=2), '\n')

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
