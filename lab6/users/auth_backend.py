from django.contrib.auth.backends import BaseBackend

from users.models import Users


class AuthBackend(BaseBackend):
    # returns a user object or None by user_id
    def get_user(self, user_id):
        user = Users.objects.raw("SELECT * FROM users WHERE id = %s",
                                 [user_id])
        user = user[0]
        return user

    # Check the username/password and return a user or None.
    def authenticate(self, request, username=None, password=None):
        user = Users.objects.raw("SELECT * FROM login_user(%s, %s)",
                                 [username, password])
        user = user[0]
        if user.id is None:
            return None
        return user
