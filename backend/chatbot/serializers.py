from rest_framework import serializers
from chatbot.models import UserInfoRecords, UserChatRecords

'''
  For Binary Fields:
    While Saving, use encode('utf-8')
    While Retrieving, use decode('utf-8')
'''

# Fields mentioned here are those which are fetched and updated 
class UserInfoRecordsSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserInfoRecords
    fields = ['user_id', 'email', 'mobile_number', 'first_name', 'last_name', 'username', 'is_premium_customer']

class UserChatRecordsSerializer(serializers.ModelSerializer):
  message = serializers.CharField()  # Use CharField for handling the query field as string
  sources = serializers.CharField() # Use CharField for handling the sources field as string

  class Meta:
    model = UserChatRecords
    fields = ['chat_id', 'user_id', 'message_request_platform', 'message_request_id', 'message', 'sources', 'feedback']

  def to_internal_value(self, data):
    # Convert strings to binary for saving
    internal_data = super().to_internal_value(data)
    if 'message' in internal_data:
      internal_data['message'] = internal_data['message'].encode('utf-8')
    if 'sources' in internal_data:
      internal_data['sources'] = internal_data['sources'].encode('utf-8')  if internal_data['sources'] is not None else None
    return internal_data

  def to_representation(self, instance):
    # Convert binary to strings for representation
    representation = super().to_representation(instance)
    if 'message' in representation:
      representation['query'] = instance.query.decode('utf-8')
    if 'sources' in representation:
    # Check if 'sources' is not None before decoding
      if instance.sources is not None:
        representation['sources'] = instance.sources.decode('utf-8')
      else:
        representation['sources'] = None  # Explicitly set to None if the value is missing
    return representation