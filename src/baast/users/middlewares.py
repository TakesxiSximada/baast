# -*- coding: utf-8 -*-
from pyramid.httpexceptions import (
    HTTPUnauthorized,
    )

from sandstorm.middlewares.core import ViewConfig
from sandstorm.middlewares.validators import Middleware
from sandstorm.middlewares.validators import ValidationMiddleware
from sandstorm.middlewares.transaction import TransactionMiddleware
from sandstorm.middlewares.responses import PyramidHTTPExceptionMiddleware

from .managers import UserManager


class AuthenticationMiddleware(Middleware):
    keywords = {
        'auth': False,
        'authentication_key': 'user_id',
        }

    def setup(self, handler):
        user_id = handler.get_secure_cookie(self.authentication_key)
        if self.auth:
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                raise HTTPUnauthorized()
            manager = UserManager()
            users = manager.get([user_id])
            if self.auth and len(users) != 1:
                raise HTTPUnauthorized()
            else:
                user = users[0]
                handler.get_current_user = lambda *args, **kwds: user


view_config = ViewConfig(
    PyramidHTTPExceptionMiddleware,
    AuthenticationMiddleware,
    TransactionMiddleware,
    ValidationMiddleware,
    )
