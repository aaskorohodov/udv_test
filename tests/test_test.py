import unittest
from unittest import TestCase, mock
from news_app.utils.db_reader import MyShinyDBReader


class TestYourClass(TestCase):
    def test_some_method(self):
        # Create an instance of the class you are testing
        instance_under_test = MyShinyDBReader()

        # Define the replacement function
        def replacement_function(*args, **kwargs):
            # Your custom logic here
            return "Mocked result"

        # Use unittest.mock.patch to replace the method with the replacement function
        with mock.patch.object(MyShinyDBReader, '_read_json', side_effect=replacement_function):
            # Call the method under test
            result = instance_under_test._read_json()

        # Assert the result
        self.assertEqual(result, "Mocked result")


if __name__ == '__main__':
    unittest.main()
