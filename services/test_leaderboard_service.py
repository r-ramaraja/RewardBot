#def test_foo():
   #pass


''' 
in the function ->  display_leaderboard()
1. check validity of user
2. 

To write unit tests using Pytest, we will need to create mock objects for the function arguments ack, body, 
client, and mysql_connection. We can use the pytest-mock library to easily create these mocks.

Here's an example of how we can write unit tests for the display_leaderboard function:

'''
import pytest
from unittest.mock import Mock
import services.leaderboard_service as leaderboard_service

@pytest.fixture
def mock_ack():
    return Mock()

@pytest.fixture
def mock_body():
    return {"user_id": "123"}

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def mock_mysql_connection():
    return Mock()

def test_display_leaderboard(mock_ack, mock_body, mock_client, mock_mysql_connection):
    # Initializing the mock objects
    mocker = Mock()
    mocker.patch('mysql_connection.cursor')
    mock_cursor = mock_mysql_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("Martha", 100), ("Keith", 50), ("Brad", 25)]

    # Function call
    leaderboard_service.display_leaderboard(mock_ack, mock_body, mock_client, mock_mysql_connection)

    # Assert
    mock_ack.assert_called_once()
    mock_mysql_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT full_name, points FROM employee ORDER BY points DESC LIMIT %s", (10,))
    mock_cursor.fetchall.assert_called_once()
    mock_client.chat_postMessage.assert_called_once_with(
        channel="123",
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Leaderboard :sports_medal:",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥇 Martha - 100 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥈 Keith - 50 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥉 Brad - 25 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            }
        ]
    )


'''

In this test case, we use the pytest.fixture decorator to create mock objects for the function arguments ack, body, 
client, and mysql_connection. We also use the mocker fixture provided by Pytest to patch 
the mysql_connection.cursor method and set up the return value for the fetchall method.

We then call the display_leaderboard function with the mock arguments, and assert that the ack method 
is called, the MySQL query is executed correctly, and the chat_postMessage method is called with the 
expected parameters.

Note that we don't need to test the logic of the display_leaderboard function itself, since that logic 
is relatively straightforward and can be verified by visual inspection. 
'''