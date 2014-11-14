# -*- coding: utf-8 -*-

from .handlers import (
    TestHandler,
    CreateHandler,
    ShowHandler,
    UpdateHandler,
    DeleteHandler,
    )


def includeme(config):
    config.add_route('/test', TestHandler, None)
    config.add_route('/new', CreateHandler, None)
    config.add_route('/show', ShowHandler, None)
    config.add_route('/update', UpdateHandler, None)
    config.add_route('/delete', DeleteHandler, None)
