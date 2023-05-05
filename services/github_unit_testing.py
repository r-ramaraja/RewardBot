import pytest
import os
import sys
import unittest
from unittest.mock import Mock

# Add the parent directory of services to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import the github_integration_service module
from services.github_integration_service import is_PR_close_event



class UTTest(unittest.TestCase):
    def test_is_PR_close_event(self):
        # Test case for a merged PR close event
        body = Mock()
        body.action = "closed"
        body.pull_request.merged = True
        body.pull_request.user.login = "dhruveel10"

        self.assertTrue(is_PR_close_event(body))

        # Test case for a closed but not merged PR
        body.action = "closed"
        body.pull_request.merged = False
        body.pull_request.user.login = "dhruveel10"

        self.assertFalse(is_PR_close_event(body))

        # Test case for an open PR
        body.action = "opened"
        body.pull_request.merged = False
        body.pull_request.user.login = "dhruveel10"

        self.assertFalse(is_PR_close_event(body))

        # # Test case for an invalid body
        # body = {}
        # with pytest.raises(KeyError):
        #     is_PR_close_event(body)
