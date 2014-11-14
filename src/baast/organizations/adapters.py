# -*- coding: utf-8 -*-
import datetime


class UserAdapter(object):
    def __init__(self, user):
        self.user = user

    @property
    def age(self):
        secret = self.user.attribute_secret
        return (datetime.datetime.now().year - secret.birth_date.year
                if secret and secret.birth_date else -1)
