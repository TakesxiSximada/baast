# -*- coding: utf-8 -*-
import json
from sandstorm.handlers import SandstormHandler
from sandstorm.decorators import (
    validate,
    view_config,
    )
from pyramid.httpexceptions import HTTPBadRequest
from .managers import UserManager
from .errors import AlreadyExistsUserError


class UserHandler(SandstormHandler):
    pass


class TestHandler(SandstormHandler):
    def get_request(self):
        import webob
        import webob.request
        environ = webob.request.environ_from_url(
            self.request.full_url())
        return webob.Request(environ)

    def get(self):
        self.write('OK')

    def post(self):
        pass


class CreateHandler(UserHandler):

    @view_config()
    @validate('schemas/user.create.request.json')
    def post(self):
        arguments = self.normalized_arguments
        name = arguments['name']
        email = arguments['email']
        password = arguments['password']
        manager = UserManager()
        try:
            user = manager.create(
                name=name, email=email, password=password)
        except AlreadyExistsUserError as err:
            raise HTTPBadRequest(str(err))
        else:
            res = {
                'status': ('o' if user else 'x'),
                }
            self.write(json.dumps(res))

class CollectionHandler(UserHandler):
    @view_config()
    @validate('schemas/user.get.request.json')
    def get(self):
        arguments = self.normalized_arguments
        try:
            user_ids = arguments['userIds']
        except KeyError:
            user_ids = []
        manager = UserManager()
        users = manager.get(user_ids)
        data = [{'id': user.id,
                 'name': user.attribute.name,
                 'email': user.attribute.email,
                 } for user in users]
        res = json.dumps(data)
        self.write(res)

class ShowHandler(UserHandler):
    schemas = {
        'get': {
            'user_ids': (int, None)
            },
        'post': {
            'user_ids': (int, None)
            },
        }

    @view_config()
    @validate('schemas/user.get.request.json')
    def get(self):
        arguments = self.normalized_arguments
        user_ids = arguments.userIds
        manager = UserManager()
        users = manager.get(user_ids)
        res = [{
            'id': user.id,
            'name': user.attribute.name,
            } for user in users]
        self.write(json.dumps(res))

    def post(self):
        params = self.parse_params()
        manager = UserManager()
        users = manager.get(params['user_ids'])
        res = [{
            'id': user.id,
            'name': user.attribute.name,
            } for user in users]
        self.write(json.dumps(res))


class UpdateHandler(UserHandler):
    @view_config()
    @validate('schemas/user.update.request.json')
    def post(self):
        arguments = self.normalized_arguments
        manager = UserManager()
        user = manager.update(**arguments)
        status = 'o' if user else 'x'
        res = {
            'status': status
            }
        self.write(json.dumps(res))


class DeleteHandler(UserHandler):
    schemas = {
        'post': {
            'user_ids': (int, None)
            },
        }

    def post(self):
        params = self.parse_params()
        user_ids = params['user_ids']

        manager = UserManager()
        delete_users = manager.delete(user_ids)
        delete_user_id_user = dict([user.id, user] for user in delete_users)

        def _build_res_entry(user_id):
            res = {
                'id': user_id,
                'name': None,
                'status': 'x',
                'reson': '???',
                }

            user = delete_user_id_user.get(user_id)
            if user:
                res['name'] = user.attribute.name,
                res['status'] = 'o'

        res = [_build_res_entry(user_id) for user_id in user_ids]
        self.write(json.dumps(res))
