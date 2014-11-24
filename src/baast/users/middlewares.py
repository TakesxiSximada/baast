# -*- coding: utf-8 -*-
from pyramid.httpexceptions import (
    HTTPUnauthorized,
    )

from sandstorm.middlewares.core import ViewConfig
from sandstorm.middlewares.validators import (
    TeadownOptionalMiddleware,
    )
from sandstorm.middlewares.validators import ValidationMiddleware
from sandstorm.middlewares.transaction import TransactionMiddleware
from sandstorm.middlewares.responses import PyramidHTTPExceptionMiddleware

from .managers import UserManager


class Authenticator(object):
    pass


class BaastAuthenticator(Authenticator):

    @property
    def auth_url(self):
        return ''

    @property
    def user(self):
        pass


class AuthenticationMiddleware(TeadownOptionalMiddleware):
    keywords = {
        'auth': 'baast',
        'authentication_key': 'user_id',
        }

    def __init__(self, *args, **kwds):
        self.redirect_url = ''
        self.auth_url = ''
        super().__init__(*args, **kwds)

    def setup(self, handler):
        user_id = handler.get_secure_cookie(self.authentication_key)
        if self.auth:
            try:
                self.redirect_url = handler.get_arguments('redirect_url')[0]
            except IndexError:
                pass

            try:
                self.auth_url = handler.get_arguments('auth_url')[0]
            except IndexError:
                pass

            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                raise HTTPUnauthorized()
            manager = UserManager()
            users = manager.get([user_id])
            if self.auth and len(users) != 1:
                if self.auth_url:
                    handler.redirect(self.redirect_url)
                else:
                    raise HTTPUnauthorized()
            else:
                user = users[0]
                handler.get_current_user = lambda *args, **kwds: user

    def teardown(self, handler):
        if self.redirect_url:
            handler.redirect(self.redirect_url)


view_config = ViewConfig(
    PyramidHTTPExceptionMiddleware,
    AuthenticationMiddleware,
    TransactionMiddleware,
    ValidationMiddleware,
    )
