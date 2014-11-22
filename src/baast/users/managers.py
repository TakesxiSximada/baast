# -*- coding: utf-8 -*-
from sqlalchemy import or_
from sqlalchemy.orm.exc import (
    NoResultFound,
    MultipleResultsFound,
    )
from .models import (
    User,
    UserAttribute,
    )
from .errors import AlreadyExistsUserError


class UserManager(object):

    def collection(self):
        return User.query().all()

    def create(self, name=None, email=None, password=None, *args, **kwds):
        user = User()
        user.save()
        attribute = UserAttribute()
        attribute.user_id = user.id

        try:
            attribute.name = name
            attribute.email = email

            # check multiple user
            already_users = User\
                .query()\
                .join(UserAttribute)\
                .filter(or_(
                    UserAttribute.name == attribute.name,
                    UserAttribute.email == attribute.email,
                    ))\
                .all()

            if already_users:
                raise AlreadyExistsUserError(
                    'name={}, email={}'.format(name, email))

            attribute.password = password
            attribute.save()
        except KeyError:
            raise
        except AlreadyExistsUserError:
            raise

        return user

    def update(self, **kwds):
        user_id = kwds['id']
        users = self.get(user_ids=[user_id])
        if len(users) == 1:
            user = users[0]
            attribute = user.attribute
            attribute.name = kwds['name']
            attribute.email = kwds['email']
            attribute.password = kwds.get('password', attribute.password)
            attribute.save()
            return user
        else:
            raise ValueError('illigal user')

    def get(self, user_ids=None):
        qs = User\
            .query()
        if user_ids:
            user_ids = list(map(int, user_ids))
            qs = qs.filter(User.id.in_(user_ids))
        return qs.all()

    def delete(self, users_or_user_ids, force=False):
        users = []
        try:
            user_ids = map(int, users_or_user_ids)
        except (ValueError, TypeError):
            users = users_or_user_ids
        else:
            users = self.get(user_ids=user_ids)

        for user in users:
            user.delete()
        return users

    def get_from_email_and_password(self, email, password):
        try:
            return User\
                .query()\
                .join(UserAttribute)\
                .filter(UserAttribute.email == email)\
                .filter(UserAttribute.password == password)\
                .one()
        except (NoResultFound, MultipleResultsFound):
            return None
