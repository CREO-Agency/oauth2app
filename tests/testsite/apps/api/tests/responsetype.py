#-*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
from urllib import urlencode
from django.utils import unittest
from django.test.client import Client as DjangoTestClient
from django_parse_rest.objects import User
from oauth2app.objects import Client
from .base import BaseTestCase


USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"


class ResponseTypeTestCase(BaseTestCase):

    user = None
    client_holder = None
    client_application = None

    def test_00_code(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_code?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" in qs)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_code?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("error" in qs)

    def test_01_token(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_token?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" in fs)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_token?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("error" in fs)

    def test_02_token_mac(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_token_mac?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("mac_key" in fs)

    def test_03_code_and_token(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" in qs)
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" not in fs)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" not in qs)
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" in fs)

    def test_04_invalid_response_type(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"blah"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("error" in qs)
