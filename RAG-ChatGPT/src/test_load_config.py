import unittest
import os
import shutil
from load_config import LoadConfig
import openai

class TestLoadConfig(unittest.TestCase):

    def setUp(self):
        self.config = LoadConfig()

    def tearDown(self):
        # Clean up any directories created during the tests
        if os.path.exists(self.config.persist_directory):
            shutil.rmtree(self.config.persist_directory)
        if os.path.exists(self.config.custom_persist_directory):
            shutil.rmtree(self.config.custom_persist_directory)

    def test_load_openai_cfg(self):
        # Ensure that the OpenAI API configuration settings are loaded correctly
        self.assertIsNotNone(openai.api_type)
        self.assertIsNotNone(openai.api_base)
        self.assertIsNotNone(openai.api_version)
        self.assertIsNotNone(openai.api_key)

    def test_create_directory(self):
        # Create a new directory and check if it exists
        directory_path = "test_directory"
        self.config.create_directory(directory_path)
        self.assertTrue(os.path.exists(directory_path))

    def test_remove_directory(self):
        # Create a new directory and then remove it
        directory_path = "test_directory"
        self.config.create_directory(directory_path)
        self.config.remove_directory(directory_path)
        self.assertFalse(os.path.exists(directory_path))

    def test_remove_directory_nonexistent(self):
        # Try to remove a directory that does not exist
        directory_path = "nonexistent_directory"
        self.config.remove_directory(directory_path)
        # Check if a message is printed indicating that the directory does not exist
        self.assertEqual(
            f"The directory '{directory_path}' does not exist.", self.config.remove_directory(directory_path))

if __name__ == '__main__':
    unittest.main()