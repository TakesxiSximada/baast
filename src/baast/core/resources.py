# -*- coding: utf-8 -*-
from zope.interface import implementer
from sqlalchemy.orm.exc import (
    NoResultFound,
    MultipleResultsFound,
    )
from .interfaces import IContext
from .models import DummyModel


class ContextMixin(object):
    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, obj):
        ifaces = self._model.implementedBy(self._model)
        if any(iface.providedBy(obj) for iface in ifaces):
            self._core = obj

    def get_from_id(self, id_):
        try:
            if hasattr(self._model, 'id'):
                id_ = int(id_)
                return self._model\
                    .query()\
                    .filter(self._model.id == id_)\
                    .one()
        except (ValueError, TypeError) as err:
            raise ValueError(err)
        except MultipleResultsFound:
            raise
        except NoResultFound:
            pass


@implementer(IContext)
class Context(ContextMixin):
    _model = DummyModel

    def __init__(self):
        self._core = None

    @classmethod
    def find(cls, condition=None):
        condition = condition if condition else cls._model.query()
        for obj in condition:
            context = cls()
            context.load(obj)
            yield context

    def new(self):
        self._core = self._model()
        return self._core

    def load(self, obj):
        ifaces = self._model.implementedBy(self._model)
        if any(iface.providedBy(obj) for iface in ifaces):
            self._core = obj
        else:
            self._core = self.get_from_id(obj)
        return self._core

    def update(self, **kwds):
        invalid_keys = [key for key in kwds
                        if not hasattr(self._core, key)]
        if invalid_keys:
            raise ValueError('Invalid keywords: {}'.format(
                ', '.join(invalid_keys)))
        for key, value in kwds.items():
            setattr(self._core, key, value)

    def delete(self):
        self._core.delete()
        return True

    def copy(self):
        obj = self._core.copy()
        context = type(self)()
        context.load(obj)
        return context

    def save(self):
        self._core.save()
        return True
