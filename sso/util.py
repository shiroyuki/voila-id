import json
import hashlib
import urllib
from tori.session.repository.base import Base as BaseSessionRepository
from sso import common

class FileSessionRepository(BaseSessionRepository):
    """ In-memory Session AbstractRepository """

    def __init__(self, location):
        self._storage  = {}
        self._location = location

        try:
            with open(self._location) as f:
                self._storage.update(json.load(f))
        except IOError:
            pass

    def delete(self, id, key):
        if not self.has(id, key):
            return

        del self._storage[id][key]

        self._update_backup()

    def get(self, id, key, auto_close=True):
        if not self.has(id, key):
            return None

        return self._storage[id][key]

    def has(self, id, key):
        return id in self._storage and key in self._storage[id]

    def registered(self, id):
        return id in self._storage

    def reset(self, id):
        del self._storage[id]

        self._update_backup()

    def set(self, id, key, content):
        if not self.registered(id):
            self._storage[id] = {}

        self._storage[id][key] = content

        self._update_backup()

    def _update_backup(self):
        with open(self._location, 'w') as f:
            json.dump(self._storage, f)

class GravatarService(object):
    email_hash_map = {}
    url_pattern    = 'http://www.gravatar.com/avatar/{email_hash}?{querystring}'

    def url(self, email, size):
        if email not in self.email_hash_map:
            self.email_hash_map[email] = hashlib.md5(email.lower()).hexdigest()

        options = {'s': str(size)}

        querystring  = urllib.urlencode(options)
        gravatar_url = self.url_pattern.format(
            email_hash  = self.email_hash_map[email],
            querystring = querystring
        )

        return gravatar_url

class Gravatar(common.Controller):
    def get(self):
        email = self.get_argument('email', None)
        size  = self.get_argument('size', None)

        if not email or not size:
            return self.set_status(400)

        gravatar_url = self.component('gravatar').url(email, size)

        self._write_json({
            'email': email,
            'size':  size,
            'url':   gravatar_url
        })

class ProfilerController(common.Controller):
    def get(self):
        self._write_json(self.session.get('auth'))