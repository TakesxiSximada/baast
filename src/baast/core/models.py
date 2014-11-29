# -*- coding: utf-8 -*-
import datetime
from zope.interface import implementer
from .interface import IModel


@implementer(IModel)
class DummyModel(object):
    name = ''
    birth_date = datetime.datetime.now()
