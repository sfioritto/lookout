from django.contrib.auth.models import User

class EmailBackend:

    """
    Authenticates against lookout users, not django
    users.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user and user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
