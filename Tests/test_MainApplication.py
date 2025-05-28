from unittest.mock import patch

from Application.MainApplication import run
from Tests.BaseTest import BaseTest


class TestMainApplication(BaseTest):

    @patch("Application.MainApplication.Casino")
    def test_main_application(self, mock_casino):
        mock_casino_instance = mock_casino.return_value
        run()

        mock_casino.assert_called_once()
        mock_casino_instance.run.assert_called_once()