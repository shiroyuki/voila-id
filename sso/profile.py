from tornado.web import HTTPError
from tori.centre import services
from sso.common import Controller, SecuredController, RestController, SecuredRestController
from sso.model.profile import Profile

class RegistrationController(Controller):
    def get(self):
        self.render('registration.html')

    def post(self):
        username       = self.get_argument('username', None)
        plain_password = self.get_argument('plain_password', None)
        name  = self.get_argument('name', None)
        email = self.get_argument('email', None)

        if not (username and plain_password and name and email):
            return self.set_status(400)

        profile_service  = self.component('profile')
        password_service = self.component('password')

        psalt = password_service.random_salt()
        phash = password_service.compute(plain_password, psalt)

        profile = profile_service.find_by_email(email)

        response = {
            'success': False
        }

        if not profile:
            profile = Profile(
                name  = name,
                email = email,
                psalt = psalt,
                phash = phash,
                username = username
            )

            profile_service.save(profile)

            response['success'] = True

        response['profile'] = {
            'id':    str(profile.id),
            'name':  profile.name,
            'email': profile.email,
            'username': profile.username
        }

        self._write_json(response)

class ProfileController(SecuredController):
    def get(self, key):
        if self._intercept(): return

        directory = self.component('profile')
        profile   = None

        if '@' in key:
            profile = directory.find_by_email(key)

            return self.redirect(self._router.resolve('user.profile', key = str(profile.id)))

        profile = directory.find_by_id(key)

        self.render(
            'profile/view.html',
            profile = profile,
            profile_rendering_data = self._convert_profile_to_rendering_data(profile)
        )

    def put(self, key):
        if not self._is_auth():
            return self.set_status(403)

        if self._auth_pass['profile']['id'] != key:
            return self.set_status(403)

        profile_service  = self.component('profile')
        password_service = self.component('password')

        profile = profile_service.find_by_id(key)

        name  = self.get_argument('name', None)
        email = self.get_argument('email', None)

        plain_password = self.get_argument('plain_password', None)

        if name:
            profile.name = name

        if email:
            profile.email = email

        if plain_password:
            profile.phash = password_service.compute(plain_password, profile.psalt)

        if name or email or plain_password:
            profile_service  = self.component('profile')
            password_service = self.component('password')

            profile_service.save(profile)

            return

        return self.set_status(201)

    def _convert_profile_to_rendering_data(self, profile):
        return [
            self._make_data_field('id', 'GUID', 'qrcode', str(profile.id), None, 'r'),
            self._make_data_field('name', 'Name', 'user', profile.name, 'text', 'rwx'),
            self._make_data_field('email', 'E-mail', 'envelope', profile.email, 'email', 'rwx'),
            self._make_data_field('plain_password', 'New Password (optional)', 'lock', None, 'password', 'w')
        ]

    def _make_data_field(self, property, label, icon, value, kind, mode):
        return {
            'property': property,
            'label':    label,
            'icon':     icon,
            'value':    value,
            'kind':     kind,
            'mode':     mode
        }