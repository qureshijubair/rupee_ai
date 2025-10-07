import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator

# Create your models here

class UserInfoRecords(AbstractUser):
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=20)
  email = models.EmailField(unique=True, validators=[EmailValidator], max_length=50)
  mobile_number = models.PositiveBigIntegerField(unique=True, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50, null=True, blank=True)
  username = models.CharField(unique=True, max_length=15)
  is_premium_customer = models.BooleanField(default=False)

  # Adding related_name to avoid clashes with the default User model
  groups = models.ManyToManyField(
    'auth.Group', related_name='custom_user_set', blank=True
  )
  user_permissions = models.ManyToManyField(
    'auth.Permission', related_name='custom_user_permissions_set', blank=True
  )
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email', 'mobile_number', 'first_name']

class UserChatRecords(models.Model):
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=20)
  user_id = models.ForeignKey(UserInfoRecords, on_delete=models.CASCADE)
  message_request_platform = models.CharField(max_length=20)
  message_request_id = models.CharField(unique=True, max_length=20)
  message = models.BinaryField()
  sources = models.BinaryField(null=True, blank=True)
  feedback = models.TextField(null=True, blank=True)



  