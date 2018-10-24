import os
import datetime
import logging
import concurrent.futures
import chess.pgn
from pgn_data_extraction import parse_thinking_time_from_comment, estimate_position, convert_result_string_to_value

logger = logging.getLogger(__file__)


def preprocess_pgn_file(input_file, output_file_end, output_file_20, output_file_40, output_file_60):
    with open(input_file, 'r') as pgn_file:
        with open(output_file_end, 'w') as csv_file_end:
            with open(output_file_20, 'w') as csv_file_20:
                with open(output_file_40, 'w') as csv_file_40:
                    with open(output_file_60, 'w') as csv_file_60:

                        processed_games_end = processed_games_20 = processed_games_40 = processed_games_60 = 0
                        total_games = 0

                        # Loop through games
                        game = chess.pgn.read_game(pgn_file)
                        while game:

                            total_games += 1
                            plyCount = int(game.headers["PlyCount"])
                            result = game.headers["Result"]

                            if not (plyCount < 2 or result not in ("1-0", "1/2-1/2", "0-1")):

                                white_elo = game.headers["WhiteElo"]
                                black_elo = game.headers["BlackElo"]
                                result_value = convert_result_string_to_value(result)
                                time_control = game.headers["TimeControl"]
                                initial_time, extra_time = map(int, time_control.split('+'))

                                white_turns_position_estimate = 0
                                white_current_time = initial_time
                                white_total_time = initial_time
                                white_used_time = 0

                                black_turns_position_estimate = 0
                                black_current_time = initial_time
                                black_total_time = initial_time
                                black_used_time = 0

                                # Loop through moves in game
                                for ply in range(plyCount):
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

                                    if (ply + 1) / 2 in (20, 40, 60) or game.is_end():

                                        # Now both players have made 20, 40 or 60 moves
                                        white_time_left_ratio = white_current_time / white_total_time
                                        black_time_left_ratio = black_current_time / black_total_time

                                        # ratings, time usage and position estimate
                                        csv_line = "{},{},{},{},{},{},{}\n".format(white_elo, black_elo,
                                                                                   white_time_left_ratio,
                                                                                   black_time_left_ratio,
                                                                                   white_turns_position_estimate,
                                                                                   black_turns_position_estimate,
                                                                                   result_value)

                                        if (ply + 1) / 2 == 20:
                                            csv_file_20.write(csv_line)
                                            processed_games_20 += 1
                                        elif (ply + 1) / 2 == 40:
                                            csv_file_40.write(csv_line)
                                            processed_games_40 += 1
                                        elif (ply + 1) / 2 == 60:
                                            csv_file_60.write(csv_line)
                                            processed_games_60 += 1
                                        elif game.is_end():
                                            # No position estimate
                                            csv_line = "{},{},{},{},{}\n".format(white_elo, black_elo,
                                                                                 white_time_left_ratio,
                                                                                 black_time_left_ratio, result_value)
                                            csv_file_end.write(csv_line)
                                            processed_games_end += 1

                            # Next game, possibly 'None'
                            game = chess.pgn.read_game(pgn_file)

    processed_games_end_percentage = 100.0 * processed_games_end / total_games
    processed_games_20_percentage = 100.0 * processed_games_20 / total_games
    processed_games_40_percentage = 100.0 * processed_games_40 / total_games
    processed_games_60_percentage = 100.0 * processed_games_60 / total_games
    return ("Processed input file {} consisting of {} games."
            "\n - {} games ({:.2f}%) into {}"
            "\n - {} games ({:.2f}%) into {}"
            "\n - {} games ({:.2f}%) into {}"
            "\n - {} games ({:.2f}%) into {}"
            ).format(input_file, total_games,
                     processed_games_end, processed_games_end_percentage, output_file_end,
                     processed_games_20, processed_games_20_percentage, output_file_20,
                     processed_games_40, processed_games_40_percentage, output_file_40,
                     processed_games_60, processed_games_60_percentage, output_file_60)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    game_files = "ficsgamesdb_{}_standard2000_movetimes.pgn"
    csv_files = "ficsgamesdb_{}_standard2000_movetimes.csv"

    print("Program starts at '{}'".format(datetime.datetime.now()))
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for date_string in list(range(2010, 2018)) + list("2018{:02}".format(MONTH) for MONTH in range(1, 10)):
            input_file = os.path.join(dir_path, "games", game_files.format(date_string))
            output_file_end = os.path.join(dir_path, "data1", csv_files.format(date_string))
            output_file_20 = os.path.join(dir_path, "data2", csv_files.format(date_string))
            output_file_40 = os.path.join(dir_path, "data3", csv_files.format(date_string))
            output_file_60 = os.path.join(dir_path, "data4", csv_files.format(date_string))
            print("Starting job for date '{}'...".format(date_string))
            futures.append(ppe.submit(preprocess_pgn_file, input_file, output_file_end, output_file_20, output_file_40,
                                      output_file_60))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    print("Program ends at '{}'".format(datetime.datetime.now()))
