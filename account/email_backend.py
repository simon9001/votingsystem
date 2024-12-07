from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Get the custom user model
        UserModel = get_user_model()
        
        try:
            # Try to get the user by email (username in this case)
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If no user is found with the given email, return None
            return None
        else:
            # Check if the password matches
            if user.check_password(password):
                return user
        return None
