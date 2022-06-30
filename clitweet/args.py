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
        "-a", "--access-token", type=str, required=True, help="Twitter access token"
    )
    parser.add_argument(
        "-t",
        "--tweet",
        type=str,
        required=True,
        help="Tweet to post. NOTE: Tweet must be text only.",
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        required=True,
        help="Twitter username",
    )
    return parser.parse_args()
