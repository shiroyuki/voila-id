# -*- coding: utf-8 -*-
from tornado.web import HTTPError
from sso import common

class AccessMode(object):
    NORMAL = 'normal'
    MASTER = 'master'

class Authentication(common.Controller):
    def get(self):
        if self.session.get('auth'):
            return self.redirect('/relay')

        app_name = self.get_argument('app', 'test')
        mode     = 'login'

        if not self._recognized_app(app_name):
            mode = 'e404'

        self.render(
            '{mode}.html'.format(mode = mode),
            app_name = app_name
        )

    def post(self):
        if self.session.get('auth'):
            return self.set_status(403)

        response = {
            'authentication': True,
            'pass': None
        }

        username = self.get_argument('key', None)
        password = self.get_argument('password', None)

        if self.settings['security']['master_access'] == username:
            response['pass'] = self._authorize_session(username, AccessMode.MASTER)

            return self._write_json(response)

        response['pass'] = self._authorize_session(username)

        self._write_json(response)

    def _authorize_session(self, username, access_mode = AccessMode.NORMAL):
        auth_pass = {
            'username':    username,
            'access_mode': access_mode,
            'avatar_url':  self.component('gravatar').url(username, 200)
        }

        self.session.set('auth', auth_pass)

        return auth_pass

    def _deauthorize_session(self, username, access_mode = AccessMode.NORMAL):
        self.session.delete('auth')

    def _recognized_app(self, app_name):
        return app_name
