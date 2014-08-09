from sso.common import Controller
from sso.security import AccessMode

class Relay(Controller):
    def get(self):
        routing_map = self.component('routing_map')

        if not self.session.get('auth'):
            return self.redirect(routing_map.resolve('authentication'))

        auth = self.session.get('auth')

        if auth['access_mode'] == AccessMode.MASTER:
            return self.redirect(routing_map.resolve('admin.profile.list'))

        if not self.session.get('referer'):
            return self.redirect(routing_map.resolve('user.profile', key = auth['username']))

        referer = self.session.get('referer')

        raise NotImplemented('To be implemented')

        return self.redirect(routing_map.resolve('authentication'))