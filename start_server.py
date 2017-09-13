# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import multiprocessing

import gunicorn.app.base

from gunicorn.six import iteritems
from app import create_app
from app.config import LocalConfig, OnlineConfig


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


config = {
	'local': LocalConfig,
	'online': OnlineConfig,
}


options = {
	'local': {
	    'bind': '%s:%s' % ('127.0.0.1', '8080'),
	    'workers': 1,
	},
	'online': {
	    'bind': '%s:%s' % ('127.0.0.1', '8080'),
	    'workers': number_of_workers(),
	    }
}


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
	env = sys.argv[1]
	if env not in ['local', 'online']:
		print('Please select env from local and online')
		exit(1)
	app = create_app(env)
	app_options = options[env]
    StandaloneApplication(app, app_options).run()