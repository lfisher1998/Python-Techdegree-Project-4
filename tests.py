# Python Techdegree Project 4 - Test File
# Developed by: Luke Fisher

import datetime
import io
import sys
import unittest
from unittest.mock import patch

from peewee import SqliteDatabase

import work_log


test_db = SqliteDatabase(':memory:', )

MODELS = [work_log.Database]


class WorkLogTests(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect(reuse_if_open=True)
        test_db.create_tables(MODELS)
        
        work_log.Database.create(employee_field="Chris", name="Task Name", time=22, notes="Notes")
        
    
    def test_invalid_time_input(self):
        with patch('builtins.input', side_effect=['','100']):
            result = work_log.get_valid_time()
        self.assertEqual(result, 100)
        
        
    def test_invalid_search_choice_input(self):
        with patch('builtins.input', side_effect=['','2']):
            result = work_log.search_entries_input()
        self.assertEqual(result, 2)
        
        
    def test_add_entry(self):
        work_log.add_entry(employee="Dave", name="Task", time=26, notes="Lots of notes")
        entry = work_log.Database(employee="Dave", time=26)
        self.assertEqual(entry.employee, "Dave")
        
    
    def test_all_dates_(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        result = work_log.all_dates()
        self.assertIn(date_str, result)
        
        
    def test_all_employees(self):
        user_input = work_log.Database.employee_field
        result = work_log.all_employees()
        self.assertIn(user_input, result)
        
        
    def test_search_by_time(self):
        test_input = 22
        result = work_log.search_by_time(test_input)
        self.assertEqual(len(result), 1)
        
        
    def test_time_query(self):
        test_input = 22
        result = work_log.time_query(test_input)
        self.assertEqual(len(result), 1) 
        
        
    def test_search_by_date(self):
        test_input = '2019-02-23'
        result = work_log.search_by_date(test_input)
        self.assertEqual(len(result), 0)
        
        
    def test_date_query(self):
        test_input = '2019-02-23'
        result = work_log.date_query(test_input)
        self.assertEqual(len(result), 0)
        
        
    def test_search_by_exact(self):
        test_input = 'Task'
        result = work_log.search_by_exact(test_input)
        self.assertEqual(len(result), 1)
        
        
    def test_exact_query(self):
        test_input = 'Task'
        result = work_log.exact_query(test_input)
        self.assertEqual(len(result), 1)
        
        
    def test_search_by_employee(self):
        test_input = 'Chris'
        result = work_log.search_by_employee(test_input)
        self.assertEqual(len(result), 1)
        
        
    def test_employee_query(self):
        test_input = 'Chris'
        result = work_log.employee_query(test_input)
        self.assertEqual(len(result), 1)  
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_entries_menu_print(self, mock_stdout):
        result = work_log.search_entries_menu()
        self.assertNotEqual(mock_stdout.getvalue(), "These are your options for searching:\n"
          "1. Search by Date\n"
          "2. Search by the Time Spent on task\n"
          "3. Search by Exact Search\n"
          "4. Search by Employee\n"
          "5. Return to Main Menu\n")
        
        
    def test_display_results_false(self):
        result = False
        results = work_log.display_results(result)
        self.assertEquals(result, 0)
        
    
    def test_display_results_one_item(self):
        results = list(work_log.Database.select())
        result = results[0]
    
        test_template = (
            "Here are your results!\n\n"
            "Employee Name: {}\n"
            "Task Name: {}\n"
            "Task Time: {}\n"
            "Task Notes: {}\n"
            "Task Date: {}\n\n"
            "\nTotal amount of matches: {}\n\n"
        ).format(result.employee_field,
            result.name, result.time, result.notes, result.date, len(results))

        with patch('sys.stdout', new_callable=io.StringIO) as mock:
            work_log.display_results(results)
            self.assertEqual(test_template, mock.getvalue())
        
    
    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()
    
    
if __name__ == '__main__':
    unittest.main()