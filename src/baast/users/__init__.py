# -*- coding: utf-8 -*-

from .handlers import (
    TestHandler,
    CollectionHandler,
    CreateHandler,
    UpdateHandler,
    DeleteHandler,
    LoginHandler,
    )


def includeme(config):
    config.add_route('/test', TestHandler, None)
    config.add_route('', CollectionHandler, None)
    config.add_route('/new', CreateHandler, None)
    config.add_route('/update', UpdateHandler, None)
    config.add_route('/delete', DeleteHandler, None)
    config.add_route('/login', LoginHandler, None)
