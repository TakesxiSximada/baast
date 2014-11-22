# -*- coding: utf-8 -*-
from sandstorm.middlewares.core import ViewConfig
from sandstorm.middlewares.validators import ValidationMiddleware
from sandstorm.middlewares.transaction import TransactionMiddleware
from sandstorm.middlewares.responses import PyramidHTTPExceptionMiddleware
view_config = ViewConfig(
    PyramidHTTPExceptionMiddleware,
    TransactionMiddleware,
    ValidationMiddleware,
    )
