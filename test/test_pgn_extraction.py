import unittest
import chess
from pgn_data_extraction import parse_thinking_time_from_comment, estimate_position, convert_result_string_to_value


class MoveTimeParsing(unittest.TestCase):
    def test_seconds_and_milliseconds(self):
        comment = "[%emt 1.234]"
        move_time = 1.234
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_hours_minutes_and_seconds(self):
        comment = "[%emt 0:05:42]"
        move_time = 5 * 60 + 42
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_hms_and_milliseconds(self):
        comment = "[%emt 1:23:45.678]"
        move_time = 1 * 60 * 60 + 23 * 60 + 45.678
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_minutes_and_seconds_only(self):
        comment = "This should [%emt 13:37] NOT work"
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertIsNone(parsed_time)

    def test_interleved_comment_and_time(self):
        comment = "[%clk 1:37:00] Beliavsky clearly suprised here takes a full [%emt 0:20:00] on this move"
        move_time = 20 * 60
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_no_move_time_in_comment(self):
        comment = "This was a brilliant move but there is no info on thinking time"
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertIsNone(parsed_time)


class PositionEstimate(unittest.TestCase):
    def test_starting_position(self):
        fen_string = chess.STARTING_BOARD_FEN
        piece_counting_value = 0
        estimate = estimate_position(fen_string)
        self.assertEqual(piece_counting_value, estimate)

    def test_one_pawn_but_stalemate(self):
        fen_string = '3k4/3P4/3K4/8/8/8/8/8'
        piece_counting_value = 1
        estimate = estimate_position(fen_string)
        self.assertEqual(piece_counting_value, estimate)

    def test_eight_white_queens_agains_two_black_rooks_and_one_bishop(self):
        fen_string = 'kr5Q/rb4Q1/5Q2/4Q3/3Q4/2Q5/1Q6/Q3K3'
        piece_counting_value = (8 * 9) - (2 * 5 + 3)
        estimate = estimate_position(fen_string)
        self.assertEqual(piece_counting_value, estimate)

    def test_fischer_spassky_1972_first_game(self):
        fen_string = '8/1p6/1P1K4/pk6/8/8/5B2/8'
        piece_counting_value = (3 + 1) - (2 * 1)
        estimate = estimate_position(fen_string)
        self.assertEqual(piece_counting_value, estimate)


class ResultStringValueConversion(unittest.TestCase):
    def test_white_wins(self):
        result = "1-0"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(1.0, result_value)

    def test_draw(self):
        result = "1/2-1/2"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(0.5, result_value)

    def test_black_wins(self):
        result = "0-1"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(0.0, result_value)


if __name__ == '__main__':
    unittest.main()
