import re
from argparse import Namespace
from io import BytesIO

from clitweet.utils.args import progArgs
from clitweet.utils.client import *
from clitweet.utils.server import *


def login(args: Namespace)  ->  None:
    secrets: tuple = secretsHandler(
        clientID=args.client_id, clientSecret=args.client_secret
    )
    redirectURI: str = buildRedirectURI(ip=args.ip, port=args.port)

    authURLData: tuple = buildAuthURL(
        clientID=secrets.clientID, redirectURI=redirectURI
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

    accessTokenData: dict = getAccessToken(
        b64Key=secrets.basicAuthKey,
        code=authCodeToken,
        redirectURI=redirectURI,
        challengeString=authChallenge,
    )
    accessToken: str = accessTokenData["access_token"]

    print(f"Save this access token somewhere as you'll need it to tweet: {accessToken}")

def post(args: Namespace)  -> None:
    resp: Response = tweet(args.tweet, args.access_token)
    match resp.status_code:
        case 401:
            print("✋ Unauthorized access. Try logging in again")
        case _:
            print("🐦 Tweet sent!")

def main() -> None:
    args: Namespace = progArgs()

    commands: dict = {
        "login": login,
        "tweet": post
    }

    option: function = commands.get(args.opt, None)
    if not option:
        print("No subcommand specified. Run clitweet -h for subcommands")
        return

    option(args)




if __name__ == "__main__":
    main()
