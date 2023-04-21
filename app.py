import os
import signal
import atexit
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import load_dotenv
from slack.award_points_events import construct_award_points_events
from slack.leaderboard_events import construct_leaderboard_events
from settings import mysql_settings

mysql_settings.init()
mysql_connection = mysql_settings.connection

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

app = construct_award_points_events(app, mysql_connection)
app = construct_leaderboard_events(app, mysql_connection)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/slack/command", methods=["POST"])
def slack_command():
    return handler.handle(request)


@flask_app.route("/slack/interactive-endpoint", methods=["POST"])
def slack_interactive():
    return handler.handle(request)


def handle_exit():
    mysql_connection.close()


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    flask_app.run(debug=True, port=3001)
