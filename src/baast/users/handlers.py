# -*- coding: utf-8 -*-
import json
from sandstorm.handlers import SandstormHandler
from pyramid.httpexceptions import HTTPBadRequest
from .managers import UserManager
from .errors import AlreadyExistsUserError
from .middlewares import view_config


class UserHandler(SandstormHandler):
    pass


class TestHandler(SandstormHandler):
    def get(self):
        self.write('OK')

    def post(self):
        self.write('OK')


class CreateHandler(UserHandler):

    @view_config(schema='schemas/user.create.request.json')
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
    @view_config(schema='schemas/user.get.request.json')
    def get(self):
        # self.set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None, **kwargs)[source]]'')
        cookie = self.get_cookie('test_cookie')
        print(cookie)
        self.set_cookie('test_cookie', 'test-gogo')
        arguments = self.normalized_arguments
        try:
            user_ids = list(map(int, arguments['userIds']))
        except KeyError:
            user_ids = []
        except (ValueError, TypeError) as err:
            raise HTTPBadRequest(err)
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

    @view_config(schema='schemas/user.get.request.json')
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
    @view_config(schema='schemas/user.update.request.json')
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

    @view_config(schema='schemas/user.delete.request.json')
    def post(self):
        print(self.request.arguments)
        arguments = self.normalized_arguments
        user_ids = [arguments['userId']]
        try:
            user_ids = list(map(int, user_ids))
        except (ValueError, TypeError) as err:
            raise HTTPBadRequest(err)
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
