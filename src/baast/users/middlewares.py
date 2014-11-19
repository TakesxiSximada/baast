# -*- coding: utf-8 -*-
from sandstorm.middlewares.core import ViewConfig
from sandstorm.middlewares.validators import ValidationMiddleware
from sandstorm.middlewares.transaction import TransactionMiddleware
view_config = ViewConfig(
    TransactionMiddleware,
    ValidationMiddleware,
    )
