import os
import pytz
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file before importing custom packages
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import Response

# Define Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')

fastapi_debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'

# Get port from environment variable or default to 8000
fastapi_port = int(os.environ.get('PORT', 8000))

fastapi_host = os.environ.get('HOST')

app = FastAPI(debug=fastapi_debug_mode, title="AI Engine API", version="0.0.1", port=fastapi_port)

# Configure logging
log_level = logging.DEBUG if fastapi_debug_mode else logging.INFO

class TimezoneFormatter(logging.Formatter):
  def converter(self, timestamp):
    # Convert timestamp to a datetime object in the given timezone
    dt = datetime.fromtimestamp(timestamp, kolkata_tz)  # Localize time to Kolkata timezone
    # Return the struct_time object needed by strftime
    return dt.timetuple()  # This is what logging.formatTime expects

# Create a custom logger
logger = logging.getLogger("ai_engine_logger")
logger.setLevel(log_level)

# Create a handler (e.g., StreamHandler for console output)
handler = logging.StreamHandler()
handler.setLevel(log_level)  # Set level for the handler

# Create a formatter with timezone support and add it to the handler
# %Z for timezone name, %z for offset
formatter = TimezoneFormatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z%z')

handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Import custom functions
from apis import router as api_router
from core.db import create_db_and_tables

# Use the combined router that includes all the sub-routers
app.include_router(api_router)

@app.get("/")
def read_root():
  logger.debug('Root endpoint accessed')
  return {"output": "Hello, World!"}

# Handle Favicon requests
@app.get("/favicon.ico")
def favicon_requests():
  return Response(status_code=204)

# app.on_event("startup")
# def on_startup():
#   create_db_and_tables()
