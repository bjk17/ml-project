import os
import re
import logging
import chess.pgn
from collections import defaultdict
from pprint import pprint

logger = logging.getLogger(__file__)


def parse_thinking_time_from_comment(comment):
    comment_regex = '\[%emt (.+?)\]'
    hhmmss_format = '\d+:[0-5][0-9]:[0-5][0-9](\.\d+)?'

    try:
        time_str = re.search(comment_regex, comment).group(1)
    except AttributeError:
        logger.debug("Comment '{}' does not contain move time.".format(comment))
        return None

    # Supporting both 'hh:mm:ss' and
    # 'seconds.milliseconds' formats
    try:
        hhmmss_str = re.search(hhmmss_format, time_str).group(0)
        h, m, s = hhmmss_str.split(':')
        return int(h) * 60 * 60 + int(m) * 60 + float(s)
    except AttributeError:
        logger.debug("Comment '{}' is not on the hh:mm:ss format.".format(comment))
        pass

    try:
        return float(time_str)
    except ValueError:
        return None


def estimate_position(fen):
    piece_values = {
        'Q': 9,
        'R': 5,
        'B': 3,
        'N': 3,
        'P': 1
    }

    white_total = sum(fen.count(piece) * piece_values[piece] for piece in piece_values)
    black_total = sum(fen.count(piece.lower()) * piece_values[piece] for piece in piece_values)

    return white_total - black_total


def count_games(pgn_file):
    with open(pgn_file, 'r') as file:
        count = 0
        while chess.pgn.read_game(file):
            count += 1
        return count


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    game_files = "ficsgamesdb_{}_standard2000_movetimes.pgn"
    pgn_file = os.path.join(dir_path, "games", game_files.format("20180101"))

    with open(pgn_file, 'r') as file:
        counter = 0
        time_controls = defaultdict(int)
        results = defaultdict(int)

        # Loop through games
        game = chess.pgn.read_game(file)
        while game:
            counter += 1

            time_control = game.headers["TimeControl"]
            time_controls[time_control] += 1
            time_left, extra_time = map(int, time_control.split('+'))

            result = game.headers["Result"]
            results[result] += 1

            # Loop through moves in game
            node = game
            while not node.is_end():
                node = node.variations[0]
                thinking_time = parse_thinking_time_from_comment(node.comment)
                time_left = time_left - thinking_time + extra_time

            game = chess.pgn.read_game(file)

        print("Number of games in dataset: {}".format(counter))
        print("Results sorted by popularity:")
        pprint(sorted(results.items(), key=lambda kv: kv[1], reverse=True))
        print("Time controls sorted by popularity:")
        pprint(sorted(time_controls.items(), key=lambda kv: kv[1], reverse=True))
