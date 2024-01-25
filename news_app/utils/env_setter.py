import io
import os


class EnvSetter:
    @staticmethod
    def set_envs(main_file_path: str) -> None:
        """Задает переменные окружения

        Args:
            main_file_path: Путь до корня с проектом

        Raises:
            FileNotFoundError: Если не нашлось файла с переменными окружения"""

        root_dir = os.path.dirname(os.path.abspath(main_file_path))
        env_file = os.path.join(root_dir, '.env')

        if not os.path.exists(env_file):
            raise FileNotFoundError(f'Файл с переменными окружения не найден! Было посмотрено сюда: {env_file}')

        with open(env_file, 'r') as f:
            variables = EnvSetter._get_vars(f)

        EnvSetter._set_envs(variables)

    @staticmethod
    def _get_vars(file: io) -> dict[str, str]:
        """Читает переменные из переданного файла и складирует их в словарь

        Умеет чистить файл от комментариев и пропускать пустые строки.

        Args:
            file: Открытый файл
        Returns:
            Словарь, куда сложит переменные и их имена"""

        variables = {}

        for line in file:
            if line != '\n' and not line.startswith('#'):
                name, value = line.strip().split('=')
                variables[name] = value.strip("'")

        return variables

    @staticmethod
    def _set_envs(variables: dict[str, str]) -> None:
        """Задает переменные окружения из переданного словаря

        Args:
            variables: Словарь в такой форме [var_name: var_value]"""

        for key, value in variables.items():
            os.environ[key] = value
