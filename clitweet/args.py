from argparse import Namespace, ArgumentParser, HelpFormatter
from operator import attrgetter

name: str = "CLI Tweet"
authors: list = ["Nicholas M. Synovic"]

class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)

def apiArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} API Experiments",
        usage="Experiments to test the HuggingFace.co REST API",
        epilog=f"Tests written by: {', '.join(authors)}",
        formatter_class=SortingHelpFormatter,
    )
    parser.add_argument("-a", "--access-token", type=str, required=True, help="Twitter access token")
    parser.add_argument("-t", "--tweet", type=str, required=True, help="Tweet to post. NOTE: Tweet must be text only.")
    return parser.parse_args()
