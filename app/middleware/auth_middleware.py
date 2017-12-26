from app.views import auth
from app.db.user_dao import UserDao
import hashlib


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path in ('/auth_begin', '/redirect'):
            response = self.get_response(request)
            return response
        email = request.COOKIES.get('useremail', None)
        if email is None:
            return auth(request)
        else:
            with UserDao() as dao:
                user = dao.get(email)
                if user is not None:
                    token = request.COOKIES.get('token')
                    expected_token = hashlib.md5((user.name + user.email).encode()).hexdigest()
                    if token != expected_token:
                        return auth(request)
                    return self.get_response(request)
                else:
                    return auth(request)

        # Code to be executed for each request/response after
        # the view is called.

