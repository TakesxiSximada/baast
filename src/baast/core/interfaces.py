# -*- coding: utf-8 -*-
from zope.interface import (
    Interface,
    )


class IModel(Interface):
    pass


class IContext(Interface):
    _model = Attribute()

    @classmethod
    def find(cls, condition):
        return [IContext()]

    def new(self):
        return IModel()

    def load(self, obj):
        return IModel()

    def update(self, **kwds):
        return True or False

    def delete(self):
        return True or False

    def save(self):
        return True or False

    def copy(self):
        return IContext()

    def __json__(self):
        return ''
