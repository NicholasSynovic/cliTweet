import re
from argparse import Namespace
from io import BytesIO

from hushtweet.utils.args import progArgs
from hushtweet.utils.client import *
from hushtweet.utils.credentials import *
from hushtweet.utils.server import *

from colorama import init as coloramaInit
from colorama import deinit as coloramaDeinit
from colorama import Fore, Style

def login(args: Namespace) -> None:
    try:
        credentials: dict = readTOML(filepath=args.config)
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

    print(f"✨ Visit this URL to authenticate:\n\n{Fore.BLUE + authURL + Style.RESET_ALL}\n")

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
        print(Fore.RED + "OAuth 2.0 authentication state verification error" + Style.RESET_ALL)
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

    writeTOML(data=credentials, filepath=args.config)

    print(Fore.GREEN + "🐦 Successfully logged into Twitter!" + Style.RESET_ALL)
    coloramaDeinit()
    quit(2)


def post(args: Namespace) -> None:
    credentials: dict = readTOML(filepath=args.config)

    resp: Response = tweet(args.tweet, credentials["accessToken"])
    match resp.status_code:
        case 401:
            print("Updating access token...")

            tokenUpdate: Response = refreshToken(
                b64Key=credentials["authKey"],
                refreshToken=credentials["refreshToken"],
                clientID=credentials["clientID"],
            )

            tokenUpdateJSON: dict = tokenUpdate.json()

            credentials["accessToken"] = tokenUpdateJSON["access_token"]
            credentials["refreshToken"] = tokenUpdateJSON["refresh_token"]

            writeTOML(data=credentials, filepath=args.config)

            print(Fore.YELLOW + "Access token has been updated. Tweet hasn't been sent." + Style.RESET_ALL)
            coloramaDeinit()

            quit(3)
        case 403:
            print(Fore.RED + "✋ Whoopsie, this is a duplicated tweet. Try being creative" + Style.RESET_ALL)
            coloramaDeinit()
            quit(4)
        case _:
            print(Fore.GREEN + "🐦 Tweet sent!" + Style.RESET_ALL)
            coloramaDeinit()
            quit(0)


def main() -> None:
    coloramaInit()

    args: Namespace = progArgs()

    commands: dict = {"login": login, "tweet": post}

    option: function = commands.get(args.opt, None)
    if not option:
        print("No subcommand specified. Run clitweet -h for subcommands")
        quit(1)

    option(args)


if __name__ == "__main__":
    main()
