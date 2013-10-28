from parse_rest.datatypes import Object, ParseField, ParseManyToManyField
from .consts import (CLIENT_KEY_LENGTH, CLIENT_SECRET_LENGTH, SCOPE_LENGTH,
        ACCESS_TOKEN_LENGTH, REFRESH_TOKEN_LENGTH, ACCESS_TOKEN_EXPIRATION,
        MAC_KEY_LENGTH, REFRESHABLE, CODE_KEY_LENGTH, CODE_EXPIRATION)
from .utils import TimestampGenerator, KeyGenerator

class Client(Object):
    name = ParseField()
    user = ParseField()
    description = ParseField()
    key = ParseField(
        default=KeyGenerator(CLIENT_KEY_LENGTH),
    )
    secret = ParseField(default=KeyGenerator(CLIENT_SECRET_LENGTH))
    redirect_uri = ParseField()


class AccessRange(Object):
    key = ParseField()
    description = ParseField()


class AccessToken(Object):
    client = ParseField()
    user = ParseField()
    token = ParseField(default=KeyGenerator(ACCESS_TOKEN_LENGTH))
    refresh_token = ParseField(default=KeyGenerator(REFRESH_TOKEN_LENGTH))
    issue = ParseField(default=TimestampGenerator())
    expire = ParseField(default=TimestampGenerator(ACCESS_TOKEN_EXPIRATION))
    refreshable = ParseField(default=REFRESHABLE)
    scope = ParseManyToManyField(AccessRange)


class Code(Object):
    client = ParseField()
    user = ParseField()
    key = ParseField(default=KeyGenerator(CODE_KEY_LENGTH))
    issue = ParseField(default=TimestampGenerator())
    expire = ParseField(default=TimestampGenerator(CODE_EXPIRATION))
    redirect_uri = ParseField()
    scope = ParseManyToManyField(AccessRange)

    def scope(self):
        #TODO should handle the M2M
        pass

class MACNonce(Object):
    access_token = ParseField()
    nonce = ParseField()
