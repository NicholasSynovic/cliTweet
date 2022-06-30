# Socket server to handle Twitter OAuth 2.0 authentication
# Docs: https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token

import random
import string
from base64 import b64encode
from collections import namedtuple
import socket
from io import BytesIO

def tokenHandler(clientID: str, clientSecret: str) -> tuple:
    authKey: str = f"{clientID}:{clientSecret}"
    byteKey: bytes = authKey.encode()
    b64Key: str = b64encode(byteKey).decode()

    data: tuple = namedtuple("TokenHandler", "clientID clientSecret, basicAuthKey")

    return data(clientID, clientSecret, b64Key)

def buildRedirectURI(ip: str, port: int)    -> str:
    return f"http://{ip}:{port}"

def buildAuthURL(
    clientID: str,
    redirectURI: str,
    scopes: list = ["tweet.read", "tweet.write", "users.read"],
    challengeLength: int = 32,
    stateLength: int = 499,
) -> tuple:
    challengeString: str = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(challengeLength)
    )
    stateString: str = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(stateLength)
    )

    return (f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope={'%20'.join(scopes)}&state={stateString}&code_challenge={challengeString}&code_challenge_method=plain", stateString)

def getAccessToken(ip: str, port: int)  ->  BytesIO:
    data: BytesIO = BytesIO()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Reuse port
        server.bind((ip, port))
        server.listen()
        conn, addr = server.accept()

        with conn:
            data.write(conn.recv(4096))
            # data.writelines(conn.recv(4096))    # TODO: Change this to not be hardcoded
            conn.close()

        server.close()

        return data

def verifyState(state: str, test: str)  ->  bool:
    if state == test:
        return True
    return False
