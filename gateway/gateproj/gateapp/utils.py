import json
import jwt
import logging
import requests
from django.conf import settings
from django.contrib.auth import authenticate

logger = logging.getLogger("gateapp")


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    logger.debug(username)
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    logger.debug(token)
    jwks = requests.get(f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json').json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = f'https://{settings.AUTH0_DOMAIN}/'
    return jwt.decode(token, public_key, audience=f'{settings.AUTH0_API_IDENTIFIER}', issuer=issuer, algorithms=['RS256'])
