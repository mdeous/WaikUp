# -*- coding: utf-8 -*-

from playhouse.migrate import Migrator

from waikup.app import app


migrator = Migrator(app.db.database)
