from argparse import ArgumentParser, HelpFormatter, Namespace
from operator import attrgetter

name: str = "CLI Tweet"
authors: list = ["Nicholas M. Synovic"]


class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def progArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name}",
        usage="Tweet from the command line",
        epilog=f"Written by: {', '.join(authors)}",
        formatter_class=SortingHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--tweet",
        type=str,
        required=True,
        help="Tweet to post. NOTE: Tweet must be text only.",
    )
    parser.add_argument(
        "-i",
        "--client-id",
        type=str,
        required=True,
        help="Twitter app OAuth 2.0 Client ID",
    )
    parser.add_argument(
        "-s",
        "--client-secret",
        type=str,
        required=True,
        help="Twitter app OAuth 2.0 Client Secret",
    )
    parser.add_argument(
        "--ip",
        type=str,
        required=False,
        default="127.0.0.1",
        help="IP address to host redirect URI. DEFAULT: 127.0.0.1",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=False,
        default="4269",
        help="Port to host redirect URI. DEFAULT: 8000",
    )
    return parser.parse_args()
