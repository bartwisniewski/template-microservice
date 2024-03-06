import os
import base64
import hashlib
import secrets
from typing import Tuple

from oauth2_client.credentials_manager import ServiceInformation, CredentialManager


scopes = ["openid", "profile", "email"]

service_information = ServiceInformation(authorize_service=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
                                         token_service=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
                                         client_id=os.environ.get("AUTH0_CLIENT_ID"),
                                         client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
                                         scopes=scopes)


manager = CredentialManager(service_information,
                            proxies=dict(http='http://localhost:8002', https='http://localhost:8002'))


def generate_sha256_pkce(length: int) -> Tuple[str, str]:
    if not (43 <= length <= 128):
        raise Exception("Invalid length: " % str(length))
    verifier = secrets.token_urlsafe(length)
    encoded = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ascii')).digest())
    challenge = encoded.decode('ascii')[:-1]
    return verifier, challenge


code_verifier, code_challenge = generate_sha256_pkce(64)
redirect_uri = "127.0.0.1/auth/callback"
authorize_url = manager.generate_authorize_url(redirect_uri, 'state_test',
                                               code_challenge=code_challenge,
                                               code_challenge_method="S256")

host = os.environ.get("API_HOST")


@jp.SetRoute('/auth/login')
def login():
    wp = jp.WebPage()
    jp.P(text="redirecting", a=wp)

    async def page_ready(self, msg):
        print("doing")
        # https://dev-v4j1hbsororundmj.eu.auth0.com/u/login?state=h
        # KFo2SBiamlWRUVlQk9oWEU4VWw5QTk1UHlTRlZVOExMRmpmcaFur
        # 3VuaXZlcnNhbC1sb2dpbqN0aWTZIHhFTE1rRl9wUGsyYzBNR042e
        # ldfS3BDdWlCYWN1WW1vo2NpZNkgVTl4VVhtcUN5RHppWm1KMjNab3hPTFFvVTlEMHh5TVo
        self.redirect = f'https://{os.environ.get("AUTH0_DOMAIN")}/u/login?state=test'
    wp.on("page_ready", page_ready)
    return wp
