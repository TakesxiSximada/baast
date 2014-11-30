# -*- coding: utf-8 -*-
import datetime
from zope.interface import implementer
import sqlalchemy as sa
from azoth.models import (
    Base,
    PowerBase,
    AUTO_INCREMENT,
    )
from .interfaces import IPersonModel
from .utils import Sex


@implementer(IPersonModel)
class User(Base, PowerBase):
    __tablename__ = 'User'
    __table_args__ = AUTO_INCREMENT,

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Unicode, default=u"")
    middle_name = sa.Column(sa.Unicode, default=u"")
    last_name = sa.Column(sa.Unicode, default=u"")
    sex = sa.Column(sa.Integer, default=Sex.unknown.value)
    birth_date = sa.Column(sa.DateTime, default=datetime.date(1900, 1, 1))

    def __eq__(self, other):
        return self.id == other.id
