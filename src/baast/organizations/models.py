# -*- coding: utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from azoth.models import (
    Base,
    SmartBase,
    PowerBase,
    AUTO_INCREMENT,
    )


class Organization(Base, PowerBase):
    __tablename__ = 'Organization'
    __table_args__ = AUTO_INCREMENT,

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode, doc=u"", default=u"")
    email = sa.Column(sa.Unicode, doc=u"", default=u"")

    def __eq__(self, other):
        return self.id == other.id


class rganizationAttribute(Base, SmartBase):
    __tablename__ = 'UserAttribute'

    user_id = sa.Column(sa.Integer, sa.ForeignKey("User.id"), primary_key=True)
    user = sa_orm.relationship('User', uselist=False, backref=sa_orm.backref('attribute', uselist=False))

    name = sa.Column(sa.Unicode, doc=u"", default=u"")
    email = sa.Column(sa.Unicode, doc=u"", default=u"")
    password = sa.Column(sa.Unicode, doc=u"", default=u"")

    first_name = sa.Column(sa.Unicode, default=u"")
    middle_name = sa.Column(sa.Unicode, default=u"")
    last_name = sa.Column(sa.Unicode, default=u"")
    address = sa.Column(sa.DateTime, nullable=True)
    birth_date = sa.Column(sa.DateTime, nullable=True)
    contact = sa.Column(sa.Unicode, default=u"")
