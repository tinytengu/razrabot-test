from unittest import TestCase as UnitTestCase


class TestCase(UnitTestCase):
    def setUp(self):
        from flask import current_app
        from project.database import setup_database

        setup_database()

        self.app = current_app
        self.app.config.update({"TESTING": True})
        self.client = self.app.test_client()
