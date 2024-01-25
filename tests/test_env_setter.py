import os
import unittest

from news_app.utils.env_setter import EnvSetter


class TestEnvSetter(unittest.TestCase):
    """Тестирует EnvSetter"""

    def setUp(self) -> None:
        test_folder_path = os.path.dirname(os.path.abspath(__file__))
        fixtures_path = os.path.join(test_folder_path, 'fixtures')
        self.env_file_path = os.path.join(fixtures_path, '.env')

        self.expected_variables = {
            'variable1': '123',
            'variable2': 'asdasd',
            'very_important_variable': 'some very important content'
        }

    def test_no_env_file(self):
        """Проверяем, что EnvSetter умеет поднимать исключение, если нет файла .env"""

        non_existent_path = os.path.join(self.env_file_path, 'something_non_existing')

        self.assertRaises(FileNotFoundError, EnvSetter.set_envs, non_existent_path)

    def test_variables_are_set(self):
        """Проверяем, что EnvSetter способен задавать переменные"""

        EnvSetter.set_envs(self.env_file_path)

        for expected_var_name, expected_value in self.expected_variables.items():
            actual_value = os.environ.get(expected_var_name)
            self.assertEqual(expected_value, actual_value)


if __name__ == '__main__':
    unittest.main()
