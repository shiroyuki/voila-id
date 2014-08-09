# -*- coding: utf-8 -*-
from tornado.web import HTTPError
from sso.common import Controller
from sso.security import AccessMode

class Deauthentication(Controller):
    def get(self):
        self.session.delete('auth')
        self.redirect(self.component('routing_map').resolve('authentication'))

class Authentication(Controller):
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
            'authenticated': True,
            'pass':          None,
            'user':          None
        }

        email    = self.get_argument('key', None)
        password = self.get_argument('password', None)

        if self.settings['security']['master_access'] == email:
            response['pass'] = self._authorize_session(email, AccessMode.MASTER)

            return self._write_json(response)

        if not (email and password):
            return self.set_status(400)

        profile_service  = self.component('profile')
        password_service = self.component('password')
        serializer       = self.component('entity.serializer')

        targeted_profile = profile_service.find_by_email(email)
        hashed_password  = password_service.compute(password, targeted_profile.psalt)
        authenticated    = targeted_profile.phash == hashed_password

        auth_pass    = None
        dict_profile = None

        if authenticated:
            dict_profile       = serializer.encode(targeted_profile)
            dict_profile['id'] = str(dict_profile['_id'])

            # Remove sensitive data
            del dict_profile['_id']
            del dict_profile['phash']
            del dict_profile['psalt']
            del dict_profile['activated']
            del dict_profile['enabled']

            auth_pass = self._authorize_session(
                email,
                AccessMode.NORMAL,
                dict_profile
            )

        response.update({
            'authenticated': authenticated,
            'pass':          auth_pass,
            'user':          dict_profile
        })

        self._write_json(response)

    def _authorize_session(self, username, access_mode, profile = None):
        auth_pass = {
            'username':    username,
            'access_mode': access_mode,
            'avatar_url':  self.component('gravatar').url(username, 200),
            'profile':     profile
        }

        self.session.set('auth', auth_pass)

        return auth_pass

    def _deauthorize_session(self, username, access_mode = AccessMode.NORMAL):
        self.session.delete('auth')

    def _recognized_app(self, app_name):
        return app_name
