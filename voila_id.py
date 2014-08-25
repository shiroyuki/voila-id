# -*- coding: utf-8 -*-

from tori.application import Application, WSGIApplication

toriapp = None
wsgiapp = None

if __name__ == '__main__':
    # Run with the built-in server.
    toriapp = Application('config/app.xml')
    toriapp.start()
else:
    # Run with Gunicorn
    toriapp = WSGIApplication('config/app.xml')
    wsgiapp = toriapp.get_backbone()
