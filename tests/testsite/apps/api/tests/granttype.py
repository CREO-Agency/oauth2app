#-*- coding: utf-8 -*-

try: import simplejson as json
except ImportError: import json
from base64 import b64encode
from django.utils import unittest
from parse_rest.user import User
from oauth2app.objects import Client
from django.test.client import Client as DjangoTestClient
from .base import BaseTestCase


USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"


class GrantTypeTestCase(BaseTestCase):

    user = None
    client_holder = None
    client_application = None

    def test_00_grant_type_client_credentials(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        client = DjangoTestClient()
        parameters = {
            "client_id": self.client_application.key,
            "grant_type": "client_credentials",
            "redirect_uri": REDIRECT_URI}
        basic_auth = b64encode("%s:%s" % (self.client_application.key,
            self.client_application.secret))
        response = client.get(
            "/oauth2/token",
            parameters,
            HTTP_AUTHORIZATION="Basic %s" % basic_auth)
        token = json.loads(response.content)
