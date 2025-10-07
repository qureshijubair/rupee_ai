from base64 import b64decode
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from chatbot.models import UserInfoRecords

# For fetching response using LLM model
from chatbot.utils import validate_query_request, get_answer

from .models import UserInfoRecords
from .serializers import UserInfoRecordsSerializer

# Create your views here

class UserInfoViewSet(viewsets.ModelViewSet):
  queryset = UserInfoRecords.objects.all()
  serializer_class = UserInfoRecordsSerializer
  permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

  def list(self, request, *args, **kwargs):
    # Only authenticated users will have access to this view
    return super().list(request, *args, **kwargs)
    
# Outputs dummy Home Page content
def home_page(request):
  return HttpResponse("Hello Developer! <br> Please use the specified API path.")

# Handle Favicon requests
def favicon_requests(request):
  return HttpResponse(status=204)

# Create a login endpoint for JWT token-based authentication
@api_view(['POST'])
def login(request):
  """
  Custom login endpoint to get JWT token for a user.
  """

  if request.method == 'POST':
    # Get credentials from the Authorization header (Basic Auth)
    auth = request.headers.get('Authorization')

    if not auth:
      raise AuthenticationFailed('Authorization header missing')

    parts = auth.split()

    if parts[0].lower() != 'basic':
      raise AuthenticationFailed('Authorization header must be Basic')

    if len(parts) == 1:
      raise AuthenticationFailed('Credentials missing')
    elif len(parts) > 2:
      raise AuthenticationFailed('Authorization header must be Basic')

    # Decode the base64 encoded credentials
    decoded = b64decode(parts[1]).decode('utf-8')
    username, password = decoded.split(':')

    try:
      # Get the user from the database
      user = UserInfoRecords.objects.get(username=username)
    except UserInfoRecords.DoesNotExist:
      return Response({"detail": "Invalid username or password."}, status=400)

    # Use check_password to verify the raw password against the stored hash
    if user.check_password(password):  # Authenticate user by password
      refresh = RefreshToken.for_user(user)
      access_token = refresh.access_token

      return Response({
        'refresh': str(refresh),
        'access': str(access_token),
      })

    return Response({"detail": "Invalid username or password."}, status=400)

# Create a new access token using JWT token-based authentication
@api_view(['POST'])
def refresh_token(request):
  """
  Endpoint to refresh the access token using the refresh token.
  """
  if request.method == 'POST':
    refresh_token = request.data.get('refresh')

    if not refresh_token:
      return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      refresh = RefreshToken(refresh_token)
      access_token = refresh.access_token
      return Response({
        'access': str(access_token),
      }, status=status.HTTP_200_OK)
    except TokenError as e:
      return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication, JWTAuthentication])
def query_api(request, format=None):
  # Sample API Request Body: 
  # {
  #   "query": {
  #     "prompt": "What is income tax?",
  #     "user_params": {
  #       "username": "vikramsamyal",
  #       "message_request_id": "mt20240822005",
  #       "message_request_platform": "web",
  #       "user_language": "english",
  #       "user_country": "india"
  #     }
  #   }
  # }

  if request.method == 'POST':
    # Extracting data from request
    raw_input_query = request.data.get('query', {}).get('prompt', '')
    raw_user_params = request.data.get('query', {}).get('user_params', {})

    # Validating input data and fetching new request payload
    request_data = validate_query_request(raw_input_query, raw_user_params, str(request.user))
    
    # Execute only if POST request if validated
    if request_data.get('validate') and (request_data.get('validate') == 'true'):
      prompt = request_data.get('prompt', '')
      user_params = request_data.get('user_params', {})
      query_output = {'response': get_answer(user_params.get('username'), prompt)}
    else:
      query_output = {'response': 'Invalid API request.'}
    
    return Response({'output': query_output}, status=status.HTTP_200_OK)
