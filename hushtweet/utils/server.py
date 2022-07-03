# Socket server to handle Twitter OAuth 2.0 authentication
# Docs: https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token

import random
import socket
import string
from base64 import b64encode
from collections import namedtuple
from io import BytesIO


def generateKey(clientID: str, clientSecret: str) -> str:
    authKey: str = f"{clientID}:{clientSecret}"
    byteKey: bytes = authKey.encode()
    return b64encode(byteKey).decode()


def buildRedirectURI(ip: str, port: int) -> str:
    return f"http://{ip}:{port}"


def buildAuthURL(
    clientID: str,
    redirectURI: str,
    scopes: list = [
        "tweet.read",
        "tweet.write",
        "users.read",
        "offline.access",
    ],
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

    return (
        f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope={'%20'.join(scopes)}&state={stateString}&code_challenge={challengeString}&code_challenge_method=plain",
        challengeString,
        stateString,
    )


def getAuthToken(ip: str, port: int) -> BytesIO:
    data: BytesIO = BytesIO()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen()
        conn, addr = server.accept()

        with conn:
            data.write(conn.recv(8192))
            conn.close()

        server.close()
    return data


def verifyState(state: str, test: str) -> bool:
    if state == test:
        return True
    return False
