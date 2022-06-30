import random
import socket
import string
from argparse import Namespace
from base64 import b64encode

from requests import Response, post

from clitweet.args import progArgs


def oauth2Authentication() -> None:
    # https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token

    clientID: str = ""
    clientSecret: str = ""
    basicAuth: str = b64encode(f"{clientID}:{clientSecret}".encode()).decode()
    print(basicAuth)

    port: int = 4269
    ip: str = "127.0.0.1"
    redirectURI: str = f"http://{ip}:{port}"
    challenge: str = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(32)
    )
    state: str = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(499)
    )
    scopes: str = "%20".join(["tweet.read", "tweet.write", "users.read"])

    # Step 1
    authURL: str = f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope={scopes}&state={state}&code_challenge={challenge}&code_challenge_method=plain"

    print(f"Visit this URL: {authURL}")

    # Step 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 4269))
        server.listen()
        conn, addr = server.accept()

        with conn:
            print(f"Connection from: {addr}")

            while True:
                data: bytes = conn.recv(2048)
                if data:
                    print(f"\n{data.decode()}\n{len(data)}")
                else:
                    break
            conn.close()

        server.close()
        print(data.decode().split("\n"))

        parsedData: list = data.decode().split("\n")[0].split(" ")[1][2:].split("&")

        respState: str = parsedData[0].replace("state=", "")
        if respState != state:
            print("OAuth2.0 state error")
            quit(2)

        # Step 3
        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basicAuth}",
        }
        data: str = f"{parsedData[1]}&grant_type=authorization_code&client_id={clientID}&redirect_uri={redirectURI}&code_verifier={challenge}"
        resp: Response = post(
            url="https://api.twitter.com/2/oauth2/token", headers=headers, data=data
        )

        print(resp.content)

    # # resp: Response = get(authURL)
    # print(resp.content)


def main() -> None:
    args: Namespace = progArgs()

    tweet: str = args.tweet.strip()

    if len(tweet) > 280:
        print(f"Tweet too long! {tweet[279:-1]}")
        quit(1)

    url: str = f"https://api.twitter.com/2/tweets"
    headers: dict = {"Authorization": f"Bearer {args.access_token}"}
    body: dict = {"text": args.tweet}
    resp: Response = post(url=url, headers=headers, data=body)
    print(resp.status_code)
    print(resp.json())


oauth2Authentication()
