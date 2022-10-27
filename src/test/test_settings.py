import unittest
# I am going to use loguru to log my tests:

# I need to import the settings.py file to see if the data is
# actually being imported properly.
import config.secrets


class TestImportSettings(unittest.TestCase):

    def test_importing_tda_apikey(self):

        pass

    def test_importing_reddit_credentials(self):

        pass
