from tornado.web import HTTPError
from sso.common import RestController

class ProfileController(RestController):
    def list(self):
        self.render('admin/profile.list.html')

    def retrieve(self, id):
        if id == 'new':
            return self.render('admin/profile.new.html')

        self.render('admin/profile.view.html')