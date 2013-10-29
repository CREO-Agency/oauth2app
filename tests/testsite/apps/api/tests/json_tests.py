#-*- coding: utf-8 -*-

try: import simplejson as json
except ImportError: import json
from .base import BaseTestCase
from django.test.client import Client as DjangoTestClient
USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"

class JSONTestCase(BaseTestCase):

    def test_00_email(self):
        client = DjangoTestClient()
        token = self.get_token()
        # Sufficient scope.
        response = client.get(
            "/api/email_json",
            {},
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["email"], USER_EMAIL)
        response = client.get(
            "/api/email_json?callback=foo",
            {},
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200)
        # Remove the JSON callback.
        content = response.content.replace("foo(", "").replace(");", "")
        self.assertEqual(json.loads(content)["email"], USER_EMAIL)
        response = client.get(
            "/api/email_json?callback=foo",
            {},
            HTTP_AUTHORIZATION="Bearer !!!%s" % token)
        content = response.content.replace("foo(", "").replace(");", "")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("error" in json.loads(content))
