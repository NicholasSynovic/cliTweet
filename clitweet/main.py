import re
from argparse import Namespace
from io import BytesIO

from clitweet.utils.args import progArgs
from clitweet.utils.client import *
from clitweet.utils.server import *


def main() -> None:
    args: Namespace = progArgs()

    tokens: tuple = tokenHandler(
        clientID=args.client_id, clientSecret=args.client_secret
    )
    redirectURI: str = buildRedirectURI(ip=args.ip, port=args.port)

    authURLData: tuple = buildAuthURL(clientID=tokens.clientID, redirectURI=redirectURI)
    authURL: str = authURLData[0]
    authState: str = authURLData[1]

    print(f"Visit this URL to authenticate:\n\n{authURL}\n")

    accessTokenBytes: BytesIO = getAuthToken(ip=args.ip, port=args.port)
    accessTokenStr: str = accessTokenBytes.getvalue().decode().strip()
    splitAccessToken: list = accessTokenStr.split("\n")

    accessToken: str = re.findall("[a-zA-Z0-9=&]+", splitAccessToken[0])[1]
    tokens: list = accessToken.replace("state=", "").replace("code=", "").split("&")
    stateToken: str = tokens[0]
    codeToken: str = tokens[1]

    if verifyState(state=authState, test=stateToken) == False:
        print("OAuth 2.0 authentication state verification error")
        quit(1)


if __name__ == "__main__":
    main()
