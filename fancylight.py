#!/usr/bin/env python
import os
from app import create_app,db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import Origin, Book, Chapter


app = create_app(os.getenv('Fanclley_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Origin=Origin,Book=Book,Chapter=Chapter)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()