import os
import datetime
import logging
import concurrent.futures
import chess.pgn
from pgn_data_extraction import parse_thinking_time_from_comment, estimate_position

logger = logging.getLogger(__file__)


def preprocess_pgn_file(input_file, output_file):
    with open(input_file, 'r') as pgn_file:
        with open(output_file, 'w') as csv_file:

            processedGames = 0
            total_games = 0

            # Loop through games
            game = chess.pgn.read_game(pgn_file)
            while game:
                total_games += 1

                if not (int(game.headers["PlyCount"]) < 40 or int(game.headers["WhiteElo"]) < 2300 or int(
                        game.headers["BlackElo"]) < 2300 or game.headers["Result"] not in ("1-0", "1/2-1/2", "0-1")):

                    processedGames += 1
                    white_elo = game.headers["WhiteElo"]
                    black_elo = game.headers["BlackElo"]
                    time_control = game.headers["TimeControl"]
                    initial_time, extra_time = map(int, time_control.split('+'))

                    result = game.headers["Result"]
                    if (result == "1/2-1/2"):
                        result_value = 0.5
                    elif (result == "1-0"):
                        result_value = 1
                    elif (result == "0-1"):
                        result_value = 0
                    else:
                        raise ValueError("Result in PGN file is '{}' which is not supported.".format(result))

                    white_turns_position_estimate = 0
                    white_current_time = initial_time
                    white_total_time = initial_time
                    white_used_time = 0

                    black_turns_position_estimate = 0
                    black_current_time = initial_time
                    black_total_time = initial_time
                    black_used_time = 0

                    # Loop through moves in game
                    for ply in range(40):
                        board = game.board()
                        next_move = game.variations[0]
                        thinking_time = parse_thinking_time_from_comment(next_move.comment)
                        if game.board().turn is chess.WHITE:
                            black_turns_position_estimate = estimate_position(board.board_fen())
                            white_used_time += thinking_time
                            white_total_time += extra_time
                            white_current_time = white_current_time - thinking_time + extra_time
                        else:
                            white_turns_position_estimate = estimate_position(board.board_fen())
                            black_used_time += thinking_time
                            black_total_time += extra_time
                            black_current_time = black_current_time - thinking_time + extra_time
                        game = next_move

                    # Now both players have made 20 moves
                    white_time_left_ratio = white_current_time / white_total_time
                    black_time_left_ratio = black_current_time / black_total_time

                    # (white_ELO, black_ELO, white_time_usage, black_time_usage, white_estimate, black_estimate, result)
                    csv_line = "{},{},{},{},{},{},{}\n".format(white_elo, black_elo, white_time_left_ratio,
                                                            black_time_left_ratio, white_turns_position_estimate,
                                                            black_turns_position_estimate, result_value)
                    csv_file.write(csv_line)

                # Next game, possibly 'None'
                game = chess.pgn.read_game(pgn_file)

    return "Processed {} games out of {} ({:.2f}%) into {}".format(processedGames, total_games,
                                                                   100 * processedGames / total_games, output_file)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    game_files = "ficsgamesdb_{}_standard2000_movetimes.pgn"
    csv_files = "ficsgamesdb_{}_standard2000_movetimes.csv"

    print("Program starts at '{}'".format(datetime.datetime.now()))
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for date_string in list(range(2010, 2018)) + list((201801,)):
            input_file = os.path.join(dir_path, "games", game_files.format(date_string))
            output_file = os.path.join(dir_path, "data3", csv_files.format(date_string))
            print("Starting job for date '{}'...".format(date_string))
            futures.append(ppe.submit(preprocess_pgn_file, input_file, output_file))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    print("Program ends at '{}'".format(datetime.datetime.now()))
