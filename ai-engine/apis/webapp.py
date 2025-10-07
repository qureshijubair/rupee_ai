import json
import pytz
import logging
from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Import custom functions
from core.db import Conversation, get_session
from core.llm import (
 generate_response
)

# Use our custom logger defined in main.py
logger = logging.getLogger("ai_engine_logger")

# Define Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')

router = APIRouter()

# Define the nested user model
class UserModel(BaseModel):
  id: str  # The mobile number string from WhatsApp

# Define the nested conversation model
class ConversationModel(BaseModel):
  platform: str  # The message origin string
  id: str  # The message id string from WhatsApp
  message: str  # The message string
  timestamp: str  # The timestamp string

# Define a model for the expected input
class InputModel(BaseModel):
  user: UserModel
  conversation: ConversationModel

@router.post("/messages/")
async def handle_messages(input_model: InputModel, session: Session = Depends(get_session)):
  # For Debugging / Logging
  logger.debug('Input Query Model: %s', input_model)

  # Extract user and conversation details from the input model
  username = input_model.user.id
  platform = input_model.conversation.platform.lower()
  message_id = input_model.conversation.id
  message_timestamp = input_model.conversation.timestamp
  message = input_model.conversation.message
  answer = ''
  
  match platform:
    case 'web':
      try:
        # Create a Conversation model instance
        input_conversation_payload = Conversation(
          message_id=message_id,
          message=message,
          platform=platform,
          author='user',
          conversation_metadata='',
          updated_on=datetime.now(kolkata_tz)
        )

        # Add conversation to the database
        session.add(input_conversation_payload)
        session.commit()
        session.refresh(input_conversation_payload)

        # Get answer
        answer = generate_response(message)

        # Create a Conversation model instance
        output_conversation_payload = Conversation(
          message_id=message_id,
          message=json.dumps(answer),
          platform=platform,
          author='bot',
          conversation_metadata='',
          updated_on=datetime.now(kolkata_tz)
        )

        # Add conversation to the database
        session.add(output_conversation_payload)
        session.commit()
        session.refresh(output_conversation_payload)
      
      except Exception as e:
        answer = f'Error occured during request processing: {e}'
        logger.error('Error occured while serving request: %s', e, exc_info=True)
      
      return {"output": answer}
    case _:
      logger.error('Request from invalid platform : %s', platform)
      raise HTTPException(status_code=400, detail="Invalid platform request")