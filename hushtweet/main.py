import re
from argparse import Namespace
from io import BytesIO

from hushtweet.utils.args import progArgs
from hushtweet.utils.client import *
from hushtweet.utils.credentials import *
from hushtweet.utils.server import *


def login(args: Namespace) -> None:
    try:
        credentials: dict = readTOML()
    except FileNotFoundError:
        credentials: dict = {
            "clientID": args.client_id,
            "clientSecret": args.client_secret,
        }

    credentials["authKey"]: str = generateKey(
        clientID=credentials["clientID"], clientSecret=credentials["clientSecret"]
    )
    redirectURI: str = buildRedirectURI(ip=args.ip, port=args.port)

    authURLData: tuple = buildAuthURL(
        clientID=credentials["clientID"], redirectURI=redirectURI
    )
    authURL: str = authURLData[0]
    authChallenge: str = authURLData[1]
    authState: str = authURLData[2]

    print(f"Visit this URL to authenticate:\n\n{authURL}\n")

    authResponse: BytesIO = (
        getAuthToken(ip=args.ip, port=args.port).getvalue().decode().strip()
    )
    authResponseComponents: list = authResponse.split("\n")
    authURIComponent: str = re.findall("[a-zA-Z0-9=&]+", authResponseComponents[0])[1]
    authTokens: list = (
        authURIComponent.replace("state=", "").replace("code=", "").split("&")
    )
    authStateToken: str = authTokens[0]
    authCodeToken: str = authTokens[1]

    if verifyState(state=authState, test=authStateToken) == False:
        print("OAuth 2.0 authentication state verification error")
        quit(1)

    accessTokenData: Response = getAccessToken(
        b64Key=credentials["authKey"],
        code=authCodeToken,
        redirectURI=redirectURI,
        challengeString=authChallenge,
    )

    accessTokenJSON: dict = accessTokenData.json()

    credentials["accessToken"]: str = accessTokenJSON["access_token"]
    credentials["refreshToken"]: str = accessTokenJSON["refresh_token"]

    writeTOML(data=credentials)

    print("🐦 Successfully logged into Twitter!")


def post(args: Namespace) -> None:
    resp: Response = tweet(args.tweet, args.access_token)
    match resp.status_code:
        case 401:
            print("✋ Unauthorized access. Try logging in again")
            quit()
        case 403:
            print("✋ Whoopsie, this is a duplicated tweet. Try being creative")
            quit()
        case _:
            print("🐦 Tweet sent!")


def main() -> None:
    args: Namespace = progArgs()

    commands: dict = {"login": login, "tweet": post}

    option: function = commands.get(args.opt, None)
    if not option:
        print("No subcommand specified. Run clitweet -h for subcommands")
        return

    option(args)


if __name__ == "__main__":
    main()
