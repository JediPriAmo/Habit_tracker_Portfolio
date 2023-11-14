#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
from unittest.mock import patch, MagicMock # Mocking is to isolate the unit tests from the real database and its interactions(More from this link https://docs.python.org/3/library/unittest.mock.html)
from io import StringIO
from Habit_tracker_script import Analytics # retrieve Analytics class from the Habit_tracker_script.py module

class TestAnalytics(unittest.TestCase):
    # assertion method: takes the 3 parameters
    # compares the actual output in the mock_stdout to the expected output
    # The output is stripped before the comparison.
    def assert_stdout(self, expected_output, mock_stdout):
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch('sys.stdout', new_callable=StringIO) # patch here temporarily replace the sys.stdout (standard output) with a StringIO object during the execution of the this function
    def test_view_all_habits(self, mock_stdout):
        with patch('Habit_tracker_script.cursor.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [
                (1, 'Exercise', 'daily', '7:00 AM', '2023-01-01', '2023-01-02'),
                (2, 'Reading', 'weekly', 'Mon,Wed,Fri', '2023-01-01', '2023-01-03')
            ]
            analytics = Analytics()
            analytics.view_all_habits()
            expected_output = "ID | Habit Name | Periodicity | Target Times/Days | Creation Date | Completed | Completion Date\n1 | Exercise | daily | 7:00 AM | 2023-01-01 | Yes | 2023-01-02\n2 | Reading | weekly | Mon,Wed,Fri | 2023-01-01 | Yes | 2023-01-03"
            self.assert_stdout(expected_output, mock_stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_longest_streaks(self, mock_stdout):
        with patch('Habit_tracker_script.cursor.execute') as mock_execute:
            mock_execute.return_value.fetchall.return_value = [
                (1, 'Exercise', 'daily'),
                (2, 'Reading', 'weekly')
            ]
            analytics = Analytics()
            analytics.view_longest_streaks()
            expected_output = "Habit Name | Periodicity | Longest Streak (Days)\nExercise | daily | 5\nReading | weekly | 3"
            self.assert_stdout(expected_output, mock_stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_longest_streak_for_habit(self, mock_stdout):
        with patch('builtins.input', side_effect=['Exercise', 'daily']):
            analytics = Analytics()
            analytics.view_longest_streak_for_habit()
            expected_output = "Longest Streak for habit 'Exercise' (Daily): 5 days"
            self.assert_stdout(expected_output, mock_stdout)

if __name__ == '__main__':
    unittest.main()

