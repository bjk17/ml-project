import unittest
from pgn_data_extraction import parse_thinking_time_from_comment


class MoveTimeParsing(unittest.TestCase):
    def test_seconds_and_milliseconds(self):
        comment = "[%emt 1.234]"
        move_time = 1.234
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_hours_minutes_and_seconds(self):
        comment = "[%emt 0:05:42]"
        move_time = 5*60 + 42
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_hms_and_milliseconds(self):
        comment = "[%emt 1:23:45.678]"
        move_time = 1*60*60 + 23*60 + 45.678
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_minutes_and_seconds_only(self):
        comment = "This should [%emt 13:37] NOT work"
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertIsNone(parsed_time)

    def test_interleved_comment_and_time(self):
        comment = "[%clk 1:37:00] Beliavsky clearly suprised here takes a full [%emt 0:20:00] on this move"
        move_time = 20*60
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertEqual(move_time, parsed_time)

    def test_no_move_time_in_comment(self):
        comment = "This was a brilliant move but there is no info on thinking time"
        parsed_time = parse_thinking_time_from_comment(comment)
        self.assertIsNone(parsed_time)



if __name__ == '__main__':
    unittest.main()
