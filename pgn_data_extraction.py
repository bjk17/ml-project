import os
import datetime
import re
import logging
import concurrent.futures
import chess.pgn

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


def convert_result_string_to_value(result):
    return float(eval(result))/2 + 0.5


def count_games(pgn_file):
    with open(pgn_file, 'r') as file:
        count = 0
        while chess.pgn.read_game(file):
            count += 1
        return count, pgn_file


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    game_files = "ficsgamesdb_{}_standard2000_movetimes.pgn"

    print("Program starts at '{}'".format(datetime.datetime.now()))
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for date_string in list(range(2010, 2018)) + list("2018{:02}".format(MONTH) for MONTH in range(1, 10)):
            input_file = os.path.join(dir_path, "games", game_files.format(date_string))
            print("Starting job for date '{}'...".format(date_string))
            futures.append(ppe.submit(count_games, input_file))

        for future in concurrent.futures.as_completed(futures):
            count, pgn_file = future.result()
            print("{} games in file {}".format(count, pgn_file))

    print("Program ends at '{}'".format(datetime.datetime.now()))
