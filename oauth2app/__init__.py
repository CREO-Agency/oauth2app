#-*- coding: utf-8 -*-


"""Django OAuth 2.0 Server Application"""

from django.conf import settings
from parse_rest.connection import register

parse_credentials = settings.PARSE_SETTINGS

for key, value in parse_credentials.items():
    del parse_credentials[key]
    parse_credentials[key.lower()] = value

register(**parse_credentials)
