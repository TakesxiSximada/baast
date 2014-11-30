# -*- coding: utf-8 -*-
from zope.interface import (
    Interface,
    Attribute,
    )


class IPersonModel(Interface):
    pass


class IPersonContext(Interface):
    _model = Attribute('_model', u'Contextとして利用する為のORMクラス')

    def find(cls, condition):
        return [IPersonContext()]

    def new(self):
        return IPersonModel()

    def load(self, obj):
        return IPersonModel()

    def update(self, **kwds):
        return True or False

    def delete(self):
        return True or False

    def save(self):
        return True or False

    def copy(self):
        return IPersonContext()

    def __json__(self):
        return ''
