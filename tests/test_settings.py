import importlib
import os
import unittest
from unittest import mock



class SettingsLazyLoadingTest(unittest.TestCase):
    def test_settings_proxy_delays_instance_creation_until_first_access(self):
        import config.settings as settings_module

        with mock.patch.dict(os.environ, {}, clear=True):
            reloaded = importlib.reload(settings_module)

            self.assertEqual(type(reloaded.settings).__name__, "_SettingsProxy")
            self.assertEqual(reloaded.settings.DATABASE_URL, "postgresql://postgres:postgres@postgres:5432/rag_db")

            first = reloaded.get_settings()
            second = reloaded.get_settings()
            self.assertIs(first, second)
            self.assertEqual(first.DATABASE_URL, reloaded.settings.DATABASE_URL)


if __name__ == "__main__":
    unittest.main()
