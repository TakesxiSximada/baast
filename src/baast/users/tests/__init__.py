# -*- coding: utf-8 -*-


def setup():
    from azoth.sessions import SessionSetup
    from azoth.models import create_all
    from .. import models
    SessionSetup.setup({
        'sqlalchemy.url': 'sqlite:///',
        })
    create_all()

def teardown():
    pass
