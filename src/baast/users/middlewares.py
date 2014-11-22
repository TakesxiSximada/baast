# -*- coding: utf-8 -*-
from sandstorm.middlewares.core import ViewConfig
from sandstorm.middlewares.validators import Middleware
from sandstorm.middlewares.validators import ValidationMiddleware
from sandstorm.middlewares.transaction import TransactionMiddleware
from sandstorm.middlewares.responses import PyramidHTTPExceptionMiddleware


class AuthenticationMiddleware(Middleware):
    pass


view_config = ViewConfig(
    AuthenticationMiddleware,
    PyramidHTTPExceptionMiddleware,
    TransactionMiddleware,
    ValidationMiddleware,
    )
