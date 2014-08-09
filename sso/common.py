# -*- coding: utf-8 -*-
import json
import os
from tori.centre import core
from tori.controller import Controller as BaseController
from tori.controller import RestController as BaseRestController

class AssetManager(object):
    def __init__(self, config):
        self._path_map = config['path_map']

    def resolve_path(self, path, kind = 'default'):
        if not kind or kind not in self._path_map:
            kind = 'default'

        return self._path_map[kind].format(path)

class Controller(BaseController):
    def initialize(self):
        self._asset_manager = AssetManager(self.settings['asset_manager'])
        self._router        = self.component('routing_map')

    def render_template(self, template_name, **contexts):
        """ Render the template with the given contexts.

            See :meth:`tori.renderer.Renderer.render` for more information on the parameters.
        """

        contexts.update({
            '_css':  self._tmpl_render_css,
            '_js':   self._tmpl_render_js,
            '_gurl': self.component('gravatar').url
        })

        return super(Controller, self).render_template(template_name, **contexts)

    def _write_json(self, response):
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        self.write(json.dumps(response))
        self.flush()

    def _get_asset_url(self, file_path, kind):
        return self._asset_manager.resolve_path(file_path, kind)

    def _tmpl_render_css(self, file_paths, kind = 'co_ext'):
        output = []

        for file_path in file_paths:
            exact_file_path = self._get_asset_url(file_path, kind)
            output.append('<link rel="stylesheet" href="{}"/>'.format(exact_file_path))

        return ''.join(output)

    def _tmpl_render_js(self, file_paths, kind = 'co_ext'):
        output = []

        for file_path in file_paths:
            exact_file_path = self._get_asset_url(file_path, kind)
            output.append('<script src="{}"></script>'.format(exact_file_path))

        return ''.join(output)

    def _recognized_app(self, app_name):
        return app_name

class RestController(BaseRestController, Controller): pass

class SecuredController(Controller):
    def prepare(self):
        self._auth_pass = self.session.get('auth')

    def _is_auth(self):
        return self._auth_pass

    def _intercept(self):
        if not self._is_auth():
            self.redirect(self._router.resolve('authentication'))

            return True

        return False

class SecuredRestController(BaseRestController, SecuredController): pass