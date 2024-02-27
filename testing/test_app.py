import os
from unittest import TestCase

from models import db, connect_db

os.environ["DATABASE_URL"] = "postgresql:///mtg-workshop-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False
