from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()  

class Environment:
    _env_variables = {}
    _instance = None

    def __init__(self):
        if Environment._instance is not None:
            raise Exception("this class is a singleton!")
        Environment._instance = self
        self._load_required_env_variables()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Environment()
        return cls._instance

    def _load_required_env_variables(self):
        required_env_variables = [
            'HOST', 'PORT'
        ]

        for variable in required_env_variables:
            env_value = os.getenv(variable)
            if env_value is None:
                raise EnvironmentError(f"{variable} environment variable is not found!")
            self._env_variables[variable] = env_value

    def __getitem__(self, key):
        return self._env_variables.get(key, None)
