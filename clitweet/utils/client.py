# REST client to get access and refresh tokens

from requests import Response, post


def getAccessToken(
    b64Key: str, code: str, redirectURI: str, challengeString: str
) -> Response:
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64Key}",
    }

    data: str = f"code={code}&grant_type=authorization_code&redirect_uri={redirectURI}&code_verifier={challengeString}"

    resp: Response = post(
        url="https://api.twitter.com/2/oauth2/token", headers=headers, data=data
    )
    return resp


def refreshToken(accessToken: str, clientID: str) -> Response:
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data: str = (
        f"refresh_token={accessToken}' &grant_type=refresh_token&client_id={clientID}"
    )

    resp: Response = post(
        url="https://api.twitter.com/2/oauth2/token", headers=headers, data=data
    )
    return resp


def tweet(text: str, accessToken: str) -> Response:
    header: dict = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {accessToken}",
    }
    body: dict = {"text": text}
    resp: Response = post("https://api.twitter.com/2/tweets", json=body, headers=header)

    return resp
